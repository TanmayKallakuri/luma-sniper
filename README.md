# 🎯 Luma Event Sniper Bot

Automatically monitor Luma events and register for events matching your interests using AI-powered event analysis.

Built with:
- **FriendliAI**: Intelligent event matching using LLM analysis
- **Opik/Comet**: Comprehensive experiment tracking and logging
- **Selenium**: Automated event registration

Perfect for hackathons, busy professionals, and event enthusiasts who don't want to miss out!

## ✨ Features

- 🤖 **AI-Powered Matching**: Uses FriendliAI to intelligently analyze events against your interests
- 📊 **Experiment Tracking**: Logs all activities to Opik/Comet for analysis
- 🔄 **Continuous Monitoring**: Runs on a schedule to catch new events
- 🎯 **Auto-Registration**: Automatically registers for relevant events
- 🔐 **Secure**: Credentials stored in environment variables
- 📝 **Detailed Logging**: Track every decision the bot makes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version)
- FriendliAI API key
- Opik/Comet API key
- Luma account

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd luma-sniper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver**

   **macOS:**
   ```bash
   brew install chromedriver
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install chromium-chromedriver
   ```

   **Or download manually:**
   - Visit https://chromedriver.chromium.org/
   - Download the version matching your Chrome browser
   - Add to PATH

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   nano .env  # or use your favorite editor
   ```

   Fill in your credentials:
   ```env
   FRIENDLI_API_KEY=your_friendli_api_key
   OPIK_API_KEY=your_opik_api_key
   LUMA_EMAIL=your_email@example.com
   LUMA_PASSWORD=your_password
   INTERESTS=AI,Machine Learning,Hackathons,Web3,Networking
   ```

5. **Test your configuration**
   ```bash
   python bot.py --test-config
   ```

### Usage

**Run once (for testing):**
```bash
python bot.py --once
```

**Run continuously:**
```bash
python bot.py
```

The bot will:
1. Discover new events on Luma
2. Analyze each event using FriendliAI
3. Automatically register for events scoring 60+ out of 100
4. Log everything to Opik/Comet
5. Wait for the configured interval and repeat

## 📋 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FRIENDLI_API_KEY` | Your FriendliAI API key | Yes | - |
| `FRIENDLI_BASE_URL` | FriendliAI API base URL | No | `https://api.friendli.ai/v1` |
| `OPIK_API_KEY` | Your Opik/Comet API key | Yes | - |
| `OPIK_WORKSPACE` | Your Opik workspace name | No | - |
| `LUMA_EMAIL` | Your Luma account email | Yes | - |
| `LUMA_PASSWORD` | Your Luma account password | Yes | - |
| `CHECK_INTERVAL_MINUTES` | Minutes between checks | No | `15` |
| `MAX_EVENTS_PER_RUN` | Max events to process per run | No | `10` |
| `INTERESTS` | Comma-separated interests | No | - |

### Customizing Interests

Edit the `INTERESTS` variable in your `.env` file:

```env
INTERESTS=AI,Machine Learning,Hackathons,Blockchain,Startup Events,Tech Talks,Networking
```

The AI will analyze events against these interests and score them accordingly.

### Scoring System

The bot uses a 0-100 scoring system:
- **80-100**: Highly relevant - definitely register
- **60-79**: Moderately relevant - probably register
- **40-59**: Somewhat relevant - maybe register (skipped by default)
- **0-39**: Not relevant - don't register

Events scoring 60+ are automatically registered.

## 🏗️ Architecture

```
luma-sniper/
├── bot.py                 # Main bot orchestration
├── luma_scraper.py       # Luma event discovery & registration
├── friendli_client.py    # FriendliAI integration
├── opik_tracker.py       # Opik/Comet tracking
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## 🎓 How It Works

1. **Event Discovery**: The bot scrapes Luma's discover page to find new events
2. **AI Analysis**: Each event is sent to FriendliAI with your interests
3. **Decision Making**: The AI provides a relevance score and recommendation
4. **Auto-Registration**: High-scoring events are automatically registered
5. **Tracking**: All actions are logged to Opik/Comet for analysis
6. **Repeat**: Process continues on a schedule

## 📊 Tracking & Analytics

The bot logs comprehensive data to Opik/Comet:

- Events discovered
- AI analysis results (scores, reasoning)
- Registration attempts (success/failure)
- Run summaries and statistics

Access your Opik/Comet dashboard to:
- Analyze which events the bot registered for
- Review AI decision-making patterns
- Track success rates over time
- Optimize your interests configuration

## 🔧 Troubleshooting

### ChromeDriver Issues

```bash
# Check Chrome version
google-chrome --version  # Linux
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version  # macOS

# Ensure ChromeDriver matches
chromedriver --version
```

### Login Failures

- Verify your Luma credentials in `.env`
- Check if Luma has CAPTCHA enabled
- Try logging in manually first

### API Errors

- Verify your FriendliAI API key is valid
- Check your FriendliAI credit balance
- Ensure Opik API key has proper permissions

### No Events Found

- Try a different location in `luma_scraper.py`
- Check Luma's website structure hasn't changed
- Increase `MAX_EVENTS_PER_RUN` in `.env`

## 🚀 Deployment

### Run in Background (Linux/macOS)

```bash
nohup python bot.py &
```

### Using Screen

```bash
screen -S luma-sniper
python bot.py
# Press Ctrl+A then D to detach
```

### Using Docker (Advanced)

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

## 🎯 Hackathon Tips

1. **Demo the AI**: Show how the bot analyzes events in real-time
2. **Show the Dashboard**: Display Opik/Comet tracking data
3. **Customize Interests**: Demo different interest profiles
4. **Success Stories**: Show events you got into that you would have missed
5. **Cost Efficiency**: Highlight using affordable FriendliAI credits

## 🤝 Contributing

This is a hackathon project, but contributions are welcome!

## 📄 License

MIT License - feel free to use for your own event sniping needs!

## 🙏 Acknowledgments

- Built with FriendliAI for intelligent event matching
- Tracked with Opik/Comet for comprehensive analytics
- Powered by Selenium for browser automation

---

Made with ❤️ for hackathons and event enthusiasts
