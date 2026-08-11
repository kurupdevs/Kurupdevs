# KurupDevs — All-in-One Telegram Bot v3.0

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful **all-in-one Telegram userbot** built with Pyrogram. Combines spam, management, fun, utility, stickers, and extra features into a single modular bot.

> Made by @kurupdevs

## Features

- **Anti-PM** — Block unwanted messages
- **AFK** — Auto-reply when away
- **Spam** — Multiple spam modes (fast, slow, big, raid, stats)
- **Management** — Kick, ban, mute, promote, pin, purge, and more
- **Fun** — Ping, alive, couples, dice, truth/dare, jokes, shayari
- **Utility** — Weather, translate, paste, currency, and more
- **Stickers** — Kang stickers, get sticker ID, sticker packs
- **Extra** — Reply, copy, forward, whisper, quote, screenshot, carbon, shorten URL, edit messages

## Setup

### Requirements
- Python 3.9 or newer
- A Telegram API ID and API Hash from my.telegram.org

### Quick Start

```bash
git clone https://github.com/kurupdevs/Kurupdevs
cd Kurupdevs
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API_ID, API_HASH
python main.py
```

## Configuration

All configuration is done through environment variables or a `.env` file:

| Variable | Description | Default |
|----------|-------------|--------|
| `API_ID` | Telegram API ID | Required |
| `API_HASH` | Telegram API Hash | Required |
| `SESSION_STRING` | Pyrogram session string | Optional |
| `DATABASE_TYPE` | Database type (`sqlite` or `mongodb`) | `sqlite` |
| `DATABASE_URL` | MongoDB connection URL | Optional |
| `DATABASE_NAME` | Database name | `kurupdevs` |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Optional |
| `GEMINI_KEY` | Google Gemini API key | Optional |
| `OPENAI_KEY` | OpenAI API key | Optional |
| `PM_LIMIT` | Anti-PM warning limit before block | `4` |
| `PREFIX` | Bot command prefix | `.` |

## Commands

| Module | Commands |
|--------|----------|
| AFK | `.afk [reason]` — Go AFK |
| Anti-PM | `.antipm` — Toggle, `.a` — Approve, `.d` — Disapprove |
| Spam | `.spam`, `.fastspam`, `.slowspam`, `.statspam`, `.delayspam`, `.bigspam`, `.raid` |
| Management | `.kick`, `.ban`, `.unban`, `.mute`, `.unmute`, `.pin`, `.unpin`, `.purge`, `.promote`, `.demote` |
| Fun | `.ping`, `.alive`, `.couples`, `.dice`, `.truth`, `.dare`, `.joke`, `.shayari`, `.figlet`, `.hug`, `.slap`, `.kiss`, `.fakeinfo` |
| Utility | `.weather`, `.tr`, `.paste`, `.currency`, `.calc`, `.whois` |
| Stickers | `.kang`, `.stickerid`, `.getsticker`, `.packinfo` |
| Extra | `.reply`, `.copy`, `.fwd`, `.whisper`, `.q`, `.webss`, `.carbon`, `.shorten`, `.edit` |

## Architecture

```
Kurupdevs/
├── main.py              # Bot entry point
├── modules/             # Feature modules
│   ├── __init__.py
│   ├── afk.py           # Away-from-keyboard
│   ├── antipm.py        # Anti-PM protection
│   ├── extra.py         # Extra utilities
│   ├── fun.py           # Fun commands
│   ├── help.py          # Help system
│   ├── management.py    # Group management
│   ├── notes.py         # Notes/snippets
│   ├── spam.py          # Spam engine
│   ├── stickers.py      # Sticker tools
│   ├── utility.py       # Utility commands
│   └── custom_modules/  # Custom module loader
├── utils/               # Core utilities
│   ├── __init__.py
│   ├── config.py        # Configuration loader
│   ├── db.py            # Database handler
│   └── scripts.py       # Helper functions
├── requirements.txt
└── .env.example
```

## Deployment

### Docker
```bash
docker build -t kurupdevs .
docker run -d --env-file .env kurupdevs
```

### Docker Compose
```bash
docker-compose up -d
```

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kurupdevs/Kurupdevs)

## License

MIT License © 2024 kurupdevs

## Contributing

Contributions are welcome! Feel free to submit a PR or open an issue.

### Development Setup

```bash
git clone https://github.com/kurupdevs/Kurupdevs
cd Kurupdevs
pip install -r requirements.txt
# For development, also install dev dependencies
pip install black isort pylint
```

---

**KurupDevs** — Your all-in-one Telegram companion.