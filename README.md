# Visa slot bot

I created this bot to get notified when screenshots are available in a Telegram channel for Dropbox appointments.

The original script `tele_visa_script.py` has been **retired** in favor of a more configurable setup using environment variables and `telegram_monitor_clean.py`.

### Prerequisites

- **Python**: 3.9+ (tested with 3.9.7)
- **Telegram account**

### 1. Clone the repo

```bash
git clone https://github.com/jimiljojo/visa-slot-bot.git
cd visa-slot-bot
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # on macOS / Linux
# .venv\Scripts\activate   # on Windows (PowerShell)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Telegram app (API credentials)

1. Go to [`https://my.telegram.org/apps`](https://my.telegram.org/apps)
2. Log in with your Telegram account
3. Create a new app and note down:
   - `API_ID`
   - `API_HASH`

### 5. Set up `.env` from the example

1. Copy the example file:

```bash
cp .env.example .env
```

2. Open `.env` and fill in:
   - `API_ID` – from step 4
   - `API_HASH` – from step 4
   - `GROUP_NAME` – the Telegram group/channel you want to monitor (e.g. `H1B_H4_Visa_Dropbox_slots`)
   - `TELEGRAM_CHAT_ID` – where notifications/images should be forwarded. Recommended formats:
     - To send to **yourself**: `me`
     - To send to a **specific user**: `@their_username`
     - To send to a **group/channel**: its `@username` (e.g. `@my_group`) or an invite link name that Telethon can resolve

> **Tip**: Raw numeric IDs (e.g. `8218400068`) may fail with `Cannot find any entity` unless that user/chat is already known in your account. Using `me` or `@username` is more reliable.

> **Note**: The real `.env` file is ignored by git and should **not** be committed. Only `.env.example` is tracked.

### 6. Run the monitor

```bash
python telegram_monitor_clean.py
```

What this script does:

- Connects to Telegram using your `API_ID` and `API_HASH`
- Monitors `GROUP_NAME` for new messages
- Sends yourself a test notification when it starts
- Forwards new images from the group to `TELEGRAM_CHAT_ID`

Keep this script running (e.g. in a terminal window or tmux/screen). When you receive notifications/images, start booking immediately.

### Legacy script

The older script `tele_visa_script.py` is kept in the repo for reference but is no longer maintained. Please use `telegram_monitor_clean.py` with `.env` and `requirements.txt` instead.

All the best, don’t lose hope!!
