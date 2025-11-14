# 🚀 Quick Start Guide

Get the Luma Sniper Bot running in 5 minutes!

## Step 1: Install Dependencies

```bash
# Run the setup script
./setup.sh
```

Or manually:
```bash
pip3 install -r requirements.txt
```

## Step 2: Get Your API Keys

### FriendliAI
1. Go to https://friendli.ai
2. Sign up / log in
3. Navigate to API settings
4. Copy your API key

### Opik/Comet
1. Go to https://www.comet.com/site/products/opik/
2. Sign up / log in
3. Get your API key from settings
4. Note your workspace name

## Step 3: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit with your credentials
nano .env
```

**Minimum required:**
```env
FRIENDLI_API_KEY=fl-xxxxxxxxxxxxx
OPIK_API_KEY=xxxxxxxxxxxxxxxx
LUMA_EMAIL=your.email@example.com
LUMA_PASSWORD=your_password
INTERESTS=AI,Machine Learning,Hackathons
```

## Step 4: Test Configuration

```bash
python3 bot.py --test-config
```

You should see: ✅ Configuration is valid!

## Step 5: Run the Bot

**Test run (processes events once):**
```bash
python3 bot.py --once
```

**Continuous mode (runs every 15 minutes):**
```bash
python3 bot.py
```

## What Happens Next?

1. Bot discovers events from Luma
2. Each event is analyzed by FriendliAI
3. High-scoring events (60+) are auto-registered
4. Everything is logged to Opik/Comet
5. You get notifications of registrations

## Troubleshooting

### "ChromeDriver not found"
```bash
# macOS
brew install chromedriver

# Ubuntu
sudo apt-get install chromium-chromedriver
```

### "Login failed"
- Double-check your Luma email/password
- Try logging in manually first
- Make sure no 2FA is enabled

### "API Error"
- Verify your FriendliAI key is correct
- Check you have remaining credits
- Ensure Opik key has proper permissions

## Demo for Hackathon

```bash
# Run once with verbose output
python3 bot.py --once

# Show the Opik dashboard
# Open https://www.comet.com/opik

# Show successful registrations
# Check your Luma account
```

## Need Help?

Check the full README.md or HACKATHON.md for detailed information!

---

Happy sniping! 🎯
