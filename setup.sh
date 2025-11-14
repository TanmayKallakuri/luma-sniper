#!/bin/bash
# Setup script for Luma Sniper Bot

echo "🎯 Luma Sniper Bot - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ $python_version"
else
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if pip is available
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 is available"
else
    echo "❌ pip3 is not installed"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for Chrome/Chromium
echo ""
echo "Checking for Chrome/Chromium..."
if command -v google-chrome &> /dev/null; then
    chrome_version=$(google-chrome --version)
    echo "✅ $chrome_version"
elif command -v chromium &> /dev/null; then
    chrome_version=$(chromium --version)
    echo "✅ $chrome_version"
elif command -v chromium-browser &> /dev/null; then
    chrome_version=$(chromium-browser --version)
    echo "✅ $chrome_version"
else
    echo "⚠️  Chrome/Chromium not found - you may need to install it"
fi

# Check for ChromeDriver
echo "Checking for ChromeDriver..."
if command -v chromedriver &> /dev/null; then
    chromedriver_version=$(chromedriver --version)
    echo "✅ $chromedriver_version"
else
    echo "⚠️  ChromeDriver not found"
    echo "   Install it with:"
    echo "   - macOS: brew install chromedriver"
    echo "   - Ubuntu: sudo apt-get install chromium-chromedriver"
    echo "   - Or download from: https://chromedriver.chromium.org/"
fi

# Setup .env file
echo ""
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your API keys and credentials"
fi

# Make bot.py executable
chmod +x bot.py

echo ""
echo "=================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your credentials:"
echo "   nano .env"
echo ""
echo "2. Test your configuration:"
echo "   python3 bot.py --test-config"
echo ""
echo "3. Run the bot:"
echo "   python3 bot.py --once    # Run once"
echo "   python3 bot.py           # Run continuously"
echo ""
echo "Happy sniping! 🎯"
