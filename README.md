# Kurupdevs
A powerful Telegram Userbot with modular architecture, web dashboard, and easy deployment.

## Features
- 🚀 Fast and lightweight
- 🧩 Modular plugin system
- 📊 Web dashboard for management
- 🐳 Docker support
- ☁️ One-click deploy to Heroku/Render

## Installation

### Docker
```bash
docker-compose up -d
```

### Manual
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

## Configuration
Edit `.env` file with your Telegram API credentials:
```
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
```

## Modules
The bot comes with various modules:
- `ping` - Check bot responsiveness
- `alive` - Bot status check
- `help` - Command help system
- And many more in the `modules/` directory

## License
MIT License - see LICENSE file
