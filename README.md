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
- **Firefox**
- **geckodriver** (in your PATH)
- **ffmpeg** (optional, for reCAPTCHA audio if needed)

### Installing dependencies by OS

<details>
<summary><b>Linux (Ubuntu / Debian)</b></summary>

```bash
sudo apt install firefox firefox-geckodriver ffmpeg
```

If `firefox-geckodriver` isn't available, download geckodriver from
https://github.com/mozilla/geckodriver/releases, extract it, and move it to `/usr/local/bin/`.

</details>

<details>
<summary><b>macOS</b></summary>

```bash
brew install --cask firefox
brew install geckodriver ffmpeg
```

</details>

<details>
<summary><b>Windows</b></summary>

1. Install **Firefox** from https://www.mozilla.org/firefox/
2. Download **geckodriver** from https://github.com/mozilla/geckodriver/releases — extract the `.exe` and add its folder to your system PATH.
3. Install **ffmpeg** from https://ffmpeg.org/download.html (or `choco install ffmpeg` if you use Chocolatey).
4. Make sure `python` and `pip` are in your PATH (install from https://www.python.org if needed).

</details>

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/jacobdcook/thm-streak-keeper.git
cd thm-streak-keeper
```

### 2. Create a virtual environment and install Python dependencies

<details>
<summary><b>Linux / macOS</b></summary>

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

</details>

<details>
<summary><b>Windows</b></summary>

```cmd
setup_venv.bat
```

Or manually:

```cmd
python -m venv .venv
.venv\Scripts\pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
```

</details>

### 3. Save your TryHackMe session

<details>
<summary><b>Linux / macOS</b></summary>

```bash
.venv/bin/python3 save_session.py
```

</details>

<details>
<summary><b>Windows</b></summary>

```cmd
.venv\Scripts\python save_session.py
```

</details>

A Firefox window opens. **Log in to TryHackMe** (email/password, Google, whatever you use). When you see your dashboard, go back to the terminal and type `done`. Your session is saved locally in `firefox_thm_profile/` — no passwords are stored anywhere.

### 4. Test it

Run with a visible browser so you can watch:

<details>
<summary><b>Linux / macOS</b></summary>

```bash
THM_HEADLESS=0 .venv/bin/python3 main_local.py
```

</details>

<details>
<summary><b>Windows (cmd)</b></summary>

```cmd
set THM_HEADLESS=0
.venv\Scripts\python main_local.py
```

</details>

<details>
<summary><b>Windows (PowerShell)</b></summary>

```powershell
$env:THM_HEADLESS="0"
.venv\Scripts\python main_local.py
```

</details>

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

### 5. Schedule it to run daily

<details>
<summary><b>Linux / macOS (cron)</b></summary>

```bash
chmod +x run_thm_streak.sh
(crontab -l 2>/dev/null; echo '0 23 * * * /path/to/thm-streak-keeper/run_thm_streak.sh') | crontab -
```

Replace `/path/to/thm-streak-keeper/` with the actual path. Runs headless every day at 11 PM.

To change the time, edit the cron expression:
- `0 7 * * *` — 7:00 AM
- `30 14 * * *` — 2:30 PM
- `0 0 * * *` — midnight

</details>

<details>
<summary><b>Windows (Task Scheduler)</b></summary>

1. Open **Task Scheduler** (search "Task Scheduler" in Start).
2. Click **Create Basic Task**.
3. Name it `THM Streak Keeper`, click Next.
4. Trigger: **Daily**, set your preferred time (e.g. 11:00 PM), click Next.
5. Action: **Start a program**.
   - Program/script: `C:\path\to\thm-streak-keeper\.venv\Scripts\python.exe`
   - Arguments: `main_local.py`
   - Start in: `C:\path\to\thm-streak-keeper`
6. Click Finish.

Make sure your computer is on (or set to wake) at the scheduled time.

</details>

### 6. Check logs

```bash
tail -30 tryhackmebot.log
```

On Windows, open `tryhackmebot.log` in any text editor, or:

```cmd
type tryhackmebot.log
```

## Run Without Your Computer (GitHub Actions)

If your computer isn't always on, you can run the streak keeper for free using GitHub Actions. The workflow runs daily on GitHub's servers — no local machine needed at run time.

### How it works

1. You run `save_session.py` **locally once** to log in and create `firefox_thm_profile/`.
2. You export that profile as a base64 string and store it as a GitHub secret.
3. A GitHub Actions workflow decodes the profile, runs the streak bot headless, and uploads logs.

### Setup

**Step 1 — Fork or clone this repo to your GitHub account.**

**Step 2 — Save your session locally** (as described above):

```bash
.venv/bin/python3 save_session.py
```

Log in, type `done`.

**Step 3 — Export the profile as base64:**

Linux / macOS:

```bash
tar czf - firefox_thm_profile | base64 -w0 > profile.b64
```

Windows (Git Bash or WSL):

```bash
tar czf - firefox_thm_profile | base64 -w0 > profile.b64
```

Windows (PowerShell):

```powershell
tar czf profile.tar.gz firefox_thm_profile
[Convert]::ToBase64String([IO.File]::ReadAllBytes("profile.tar.gz")) | Set-Content profile.b64 -NoNewline
```

**Step 4 — Add the secret to your repo:**

1. Open your repo on GitHub.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret**.
4. Name: `THM_PROFILE_B64`
5. Value: paste the contents of `profile.b64`.
6. Click **Add secret**.

**Step 5 — Enable the workflow:**

Go to the **Actions** tab in your repo. If prompted, enable workflows. The `THM Streak Keeper (Cloud)` workflow will run daily. You can also trigger it manually with **Run workflow**.

### When your session expires

If the bot logs show `[!] Not logged in`, your session has expired. Repeat steps 2-4: run `save_session.py`, export the profile, and update the `THM_PROFILE_B64` secret.

> **Note:** GitHub Actions runs from different IPs each time, so TryHackMe sessions may expire faster than on your local machine. If this happens frequently, the local cron approach is more reliable.

## Session Expired?

If you see `[!] Not logged in`, your TryHackMe session expired. Just run `save_session.py` again, log in, and type `done`. For the GitHub Actions option, also re-export and re-upload the profile secret.

## Important

- **Join the [polkit room](https://tryhackme.com/room/polkit)** on TryHackMe before running the bot.
- For local runs, your computer needs to be on at the scheduled time.
- For GitHub Actions runs, your computer does not need to be on — but you need to re-upload the session when it expires.
- This is for **maintaining** a streak on days you aren't doing rooms. It's not a replacement for actually learning.

## Files

| File | Purpose |
|---|---|
| `save_session.py` | Opens Firefox for you to log in. Saves the session. |
| `main_local.py` | Runs the streak keeper using the saved session. |
| `keepstreak.py` | The logic: reset room, click Check, read streak. |
| `run_thm_streak.sh` | Shell wrapper for cron (Linux/macOS, headless). |
| `setup_venv.sh` | Creates venv and installs deps (Linux/macOS). |
| `setup_venv.bat` | Creates venv and installs deps (Windows). |
| `requirements.txt` | Python dependencies. |
| `.github/workflows/thmbot-cloud.yml` | GitHub Actions workflow (optional, run without your PC). |
