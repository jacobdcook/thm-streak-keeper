# THM Streak Keeper

A simple Selenium-based tool that maintains your TryHackMe streak by running once a day. **This does not solve rooms or complete challenges for you** — it only resets and re-answers a single free question in the [polkit room](https://tryhackme.com/room/polkit) to keep your streak alive.

I built this after losing my streak. I tried a few existing bots out there but none of them worked — they were outdated and the TryHackMe page layout had changed. So I made this one with current (Feb 2026) selectors and a simple session-based approach: you log in once in a real browser, the session is saved, and a headless cron job handles the rest.

## What It Does

1. Opens TryHackMe using your saved browser session (no stored passwords).
2. Navigates to the polkit room.
3. Resets room progress.
4. Clicks "Check" on the first question to register activity.
5. Reads your updated streak counter.

That's it. One room, one question, once a day. Enough to keep your streak going on weekends or days you aren't doing rooms.

## Requirements

- **Python 3.10+**
- **Firefox** (installed on your system)
- **geckodriver** (in your PATH)
- **ffmpeg** (optional, for reCAPTCHA audio if needed)
- Linux (tested on Ubuntu/Debian). Should work on other distros. Might work on macOS with tweaks.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/jacobdcook/thm-streak-keeper.git
cd thm-streak-keeper
```

### 2. Create a virtual environment and install dependencies

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### 3. Save your TryHackMe session

```bash
.venv/bin/python3 save_session.py
```

A Firefox window opens. **Log in to TryHackMe** (email/password, Google, whatever you use). When you see your dashboard, go back to the terminal and type `done`. Your session is saved locally in `firefox_thm_profile/` — no passwords are stored anywhere.

### 4. Test it

With a visible browser (so you can watch):

```bash
THM_HEADLESS=0 .venv/bin/python3 main_local.py
```

You should see:

```
[+] Starting (local, persistent profile)...
[+] Session valid, running streak...
[+] Navigated to polkit room
[+] Reset progress clicked
[+] Check / submit button clicked
[+] Success! Your Streak is 1
[+] Closing...
```

### 5. Schedule it (daily via cron)

```bash
chmod +x run_thm_streak.sh
(crontab -l 2>/dev/null; echo '0 23 * * * /path/to/thm-streak-keeper/run_thm_streak.sh') | crontab -
```

Replace `/path/to/thm-streak-keeper/` with wherever you cloned the repo. It will run headless every day at 11 PM.

To change the time, edit the cron expression. Examples:
- `0 7 * * *` — 7:00 AM
- `30 14 * * *` — 2:30 PM
- `0 0 * * *` — midnight

### 6. Check logs

```bash
tail -30 tryhackmebot.log
```

## Session Expired?

If you see `[!] Not logged in`, your TryHackMe session expired. Just run `save_session.py` again, log in, and type `done`. No password changes needed.

## Important

- **Join the [polkit room](https://tryhackme.com/room/polkit)** on TryHackMe before running the bot.
- Your computer needs to be on at the scheduled time (this runs locally, not in the cloud).
- This is for **maintaining** a streak on days you aren't doing rooms. It's not a replacement for actually learning.

## Files

| File | Purpose |
|---|---|
| `save_session.py` | Opens Firefox for you to log in. Saves the session. |
| `main_local.py` | Runs the streak keeper using the saved session. |
| `keepstreak.py` | The logic: reset room, click Check, read streak. |
| `run_thm_streak.sh` | Shell wrapper for cron (headless). |
| `setup_venv.sh` | Creates venv and installs Python deps. |
| `requirements.txt` | Python dependencies. |
