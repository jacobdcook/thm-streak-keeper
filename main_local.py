"""
Local THM streak bot. Uses persistent Firefox profile from save_session.py.
Run daily via cron after 11pm (run_thm_streak.sh).
"""
import os
import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(SCRIPT_DIR, "firefox_thm_profile")
LOG_FILE = os.path.join(SCRIPT_DIR, "tryhackmebot.log")


def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{msg}\n")
    print(msg)


def is_logged_in(driver):
    driver.get("https://tryhackme.com/hacktivities")
    time.sleep(5)
    url = driver.current_url.lower()
    if "login" in url:
        return False
    return True


def main():
    os.chdir(SCRIPT_DIR)
    headless = os.environ.get("THM_HEADLESS", "1") == "1"

    if not os.path.exists(PROFILE_DIR):
        log("[!] No profile yet. Run:  .venv/bin/python3 save_session.py")
        sys.exit(1)

    options = Options()
    options.add_argument("-profile")
    options.add_argument(PROFILE_DIR)
    if headless:
        options.add_argument("--headless")
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference("dom.webnotifications.enabled", False)

    try:
        driver = webdriver.Firefox(options=options)
    except Exception as e:
        log(f"[!] Error starting Firefox: {e}")
        sys.exit(1)

    driver.implicitly_wait(15)

    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}\n")
    log("[+] Starting (local, persistent profile)...")

    try:
        from keepstreak import keep_streak

        if is_logged_in(driver):
            log("[+] Session valid, running streak...")
            keep_streak(driver)
        else:
            log("[!] Not logged in. Run:  .venv/bin/python3 save_session.py")
    except Exception as e:
        log(f"[!] Fatal error: {e}")
    finally:
        log("[+] Closing...")
        driver.quit()


if __name__ == "__main__":
    main()
