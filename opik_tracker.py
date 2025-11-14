"""Opik/Comet integration for experiment tracking."""
from typing import Dict, Any
import json
from datetime import datetime


class OpikTracker:
    """Tracker for logging bot activities to Opik/Comet."""

    def __init__(self):
        self.current_run = None
        self.events_processed = 0
        self.events_registered = 0
        self._initialize_opik()

    def _initialize_opik(self):
        """Initialize Opik client."""
        try:
            import opik
            from config import Config

            opik.configure(api_key=Config.OPIK_API_KEY)
            self.client = opik.Opik()
            print("✅ Opik tracker initialized")
        except Exception as e:
            print(f"⚠️  Opik initialization failed: {e}")
            print("   Continuing without tracking...")
            self.client = None

    def start_run(self, run_name: str = None):
        """Start a new tracking run."""
        if not self.client:
            return

        try:
            if run_name is None:
                run_name = f"luma_sniper_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            self.current_run = {
                "name": run_name,
                "start_time": datetime.now().isoformat(),
                "events_found": 0,
                "events_analyzed": 0,
                "events_registered": 0,
                "events_skipped": 0,
            }
            print(f"📊 Started tracking run: {run_name}")
        except Exception as e:
            print(f"⚠️  Failed to start Opik run: {e}")

    def log_event_discovered(self, event_data: Dict):
        """Log when a new event is discovered."""
        if self.current_run:
            self.current_run["events_found"] += 1

        self._log_to_console("EVENT_DISCOVERED", event_data)

    def log_event_analysis(self, event_data: Dict, analysis: Dict):
        """Log event analysis results."""
        if self.current_run:
            self.current_run["events_analyzed"] += 1

        log_data = {
            "event_title": event_data.get("title"),
            "event_url": event_data.get("url"),
            "score": analysis.get("score"),
            "reasoning": analysis.get("reasoning"),
            "decision": "REGISTER" if analysis.get("should_register") else "SKIP",
        }

        self._log_to_console("EVENT_ANALYSIS", log_data)
        self._log_to_opik("event_analysis", log_data)

    def log_registration_attempt(self, event_data: Dict, success: bool, error: str = None):
        """Log event registration attempt."""
        if self.current_run:
            if success:
                self.current_run["events_registered"] += 1
            else:
                self.current_run["events_skipped"] += 1

        log_data = {
            "event_title": event_data.get("title"),
            "event_url": event_data.get("url"),
            "success": success,
            "error": error,
        }

        self._log_to_console("REGISTRATION", log_data)
        self._log_to_opik("registration", log_data)

    def end_run(self):
        """End the current tracking run."""
        if not self.current_run:
            return

        try:
            self.current_run["end_time"] = datetime.now().isoformat()
            print(f"\n📊 Run Summary:")
            print(f"   Events Found: {self.current_run['events_found']}")
            print(f"   Events Analyzed: {self.current_run['events_analyzed']}")
            print(f"   Events Registered: {self.current_run['events_registered']}")
            print(f"   Events Skipped: {self.current_run['events_skipped']}")

            self._log_to_opik("run_summary", self.current_run)
        except Exception as e:
            print(f"⚠️  Failed to end Opik run: {e}")
        finally:
            self.current_run = None

    def _log_to_console(self, event_type: str, data: Dict):
        """Log to console for debugging."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {event_type}: {json.dumps(data, indent=2)}")

    def _log_to_opik(self, event_type: str, data: Dict):
        """Log data to Opik."""
        if not self.client:
            return

        try:
            # Log as a trace in Opik using the client
            trace = self.client.trace(
                name=event_type,
                input=data,
                output={"status": "logged"},
                metadata={"timestamp": datetime.now().isoformat()},
            )
            trace.end()
        except Exception as e:
            print(f"⚠️  Failed to log to Opik: {e}")
