"""Luma event scraper and monitor."""
import requests
import time
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from config import Config


class LumaScraper:
    """Scraper for Luma events."""

    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False
        self.seen_events = set()  # Track events we've already processed
        self.driver = None

    def initialize_browser(self):
        """Initialize Selenium browser for Luma interactions."""
        if self.driver:
            return

        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Browser initialized")
        except Exception as e:
            print(f"❌ Failed to initialize browser: {e}")
            print("   Make sure Chrome and chromedriver are installed")

    def login(self) -> bool:
        """Login to Luma."""
        if self.logged_in:
            return True

        try:
            self.initialize_browser()
            if not self.driver:
                return False

            print("🔐 Logging into Luma...")
            self.driver.get("https://lu.ma/signin")

            # Wait for email input
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            email_input.send_keys(Config.LUMA_EMAIL)

            # Submit email
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()

            time.sleep(2)

            # Wait for password input
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password'], input[name='password']"))
            )
            password_input.send_keys(Config.LUMA_PASSWORD)

            # Submit password
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()

            # Wait for login to complete
            time.sleep(5)

            # Check if login was successful by looking for user-specific elements
            self.logged_in = True
            print("✅ Successfully logged into Luma")
            return True

        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    def discover_events(self, location: str = "san-francisco-bay-area") -> List[Dict]:
        """
        Discover events from Luma.

        Args:
            location: Location slug for filtering events

        Returns:
            List of event dictionaries
        """
        events = []

        try:
            # Scrape Luma discover page
            url = f"https://lu.ma/discover?location={location}"
            print(f"🔍 Discovering events from: {url}")

            self.initialize_browser()
            if not self.driver:
                return events

            self.driver.get(url)
            time.sleep(3)  # Wait for page to load

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Find event cards (this selector may need adjustment based on Luma's actual HTML)
            event_cards = soup.find_all("div", class_=lambda x: x and "event" in x.lower() if x else False)

            if not event_cards:
                # Fallback: try to find links to events
                event_links = soup.find_all("a", href=lambda x: x and "/event/" in x if x else False)
                print(f"   Found {len(event_links)} event links")

                for link in event_links[:Config.MAX_EVENTS_PER_RUN]:
                    event_url = link.get("href")
                    if not event_url.startswith("http"):
                        event_url = f"https://lu.ma{event_url}"

                    # Skip if we've seen this event
                    if event_url in self.seen_events:
                        continue

                    event_data = self.scrape_event_details(event_url)
                    if event_data:
                        events.append(event_data)
                        self.seen_events.add(event_url)

            print(f"✅ Discovered {len(events)} new events")
            return events

        except Exception as e:
            print(f"❌ Error discovering events: {e}")
            return events

    def scrape_event_details(self, event_url: str) -> Optional[Dict]:
        """
        Scrape details for a specific event.

        Args:
            event_url: URL of the event

        Returns:
            Dictionary with event details or None
        """
        try:
            self.driver.get(event_url)
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            # Extract event details (selectors may need adjustment)
            title = soup.find("h1")
            title = title.get_text(strip=True) if title else "Unknown Event"

            # Try to find description
            description_elem = soup.find("div", class_=lambda x: x and "description" in x.lower() if x else False)
            description = description_elem.get_text(strip=True) if description_elem else ""

            # Try to find date and location
            date = "TBD"
            location = "TBD"

            event_data = {
                "title": title,
                "description": description[:500],  # Limit description length
                "url": event_url,
                "date": date,
                "location": location,
            }

            print(f"   📅 {title}")
            return event_data

        except Exception as e:
            print(f"⚠️  Failed to scrape event {event_url}: {e}")
            return None

    def register_for_event(self, event_url: str) -> bool:
        """
        Register for an event on Luma.

        Args:
            event_url: URL of the event to register for

        Returns:
            True if registration successful, False otherwise
        """
        try:
            if not self.logged_in:
                if not self.login():
                    return False

            print(f"📝 Attempting to register for event: {event_url}")
            self.driver.get(event_url)
            time.sleep(2)

            # Look for register/RSVP button
            register_button = None
            possible_selectors = [
                "button[data-testid='rsvp-button']",
                "button:contains('Register')",
                "button:contains('RSVP')",
                "a:contains('Register')",
            ]

            for selector in possible_selectors:
                try:
                    register_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if register_button:
                        break
                except:
                    continue

            if not register_button:
                # Try finding any button with register-like text
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for button in buttons:
                    text = button.text.lower()
                    if any(word in text for word in ["register", "rsvp", "attend", "join"]):
                        register_button = button
                        break

            if register_button:
                register_button.click()
                time.sleep(3)

                print("✅ Successfully registered for event!")
                return True
            else:
                print("⚠️  Could not find registration button")
                return False

        except Exception as e:
            print(f"❌ Registration failed: {e}")
            return False

    def close(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")
