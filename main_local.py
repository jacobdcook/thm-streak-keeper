"""
Local THM streak bot. Uses persistent Firefox profile from save_session.py, or
thm_cookies.json when present (e.g. GitHub Actions with THM_COOKIES_B64).
"""
import json
import os
import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(SCRIPT_DIR, "firefox_thm_profile")
COOKIES_FILE = os.path.join(SCRIPT_DIR, "thm_cookies.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "tryhackmebot.log")


def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"{msg}\n")
    print(msg)


def load_cookies(driver):
    if not os.path.exists(COOKIES_FILE):
        return False
    try:
        driver.get("https://tryhackme.com")
        with open(COOKIES_FILE) as f:
            cookies = json.load(f)
        for c in cookies:
            try:
                add = {"name": c["name"], "value": c["value"]}
                if c.get("path"):
                    add["path"] = c["path"]
                if c.get("domain"):
                    add["domain"] = c["domain"]
                if "secure" in c:
                    add["secure"] = bool(c["secure"])
                if "httpOnly" in c:
                    add["httpOnly"] = bool(c["httpOnly"])
                if "expiry" in c:
                    add["expiry"] = int(c["expiry"])
                if c.get("sameSite") == "None":
                    add["secure"] = True
                if c.get("sameSite") in ("Lax", "Strict", "None"):
                    add["sameSite"] = c["sameSite"]
                driver.add_cookie(add)
            except Exception:
                pass
        driver.refresh()
        return True
    except Exception:
        return False


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
    use_cookies = os.path.exists(COOKIES_FILE)

    options = Options()
    if use_cookies:
        pass
    else:
        if not os.path.exists(PROFILE_DIR):
            log("[!] No profile and no thm_cookies.json. Run save_session.py or add THM_COOKIES_B64 in Actions.")
            sys.exit(1)
        options.add_argument("-profile")
        options.add_argument(PROFILE_DIR)
    if headless:
        options.add_argument("--headless")
    options.set_preference("media.volume_scale", "0.0")
    options.set_preference("dom.webnotifications.enabled", False)
    firefox_bin = os.environ.get("FIREFOX_BIN")
    if firefox_bin:
        options.binary_location = firefox_bin

    service = None
    geckodriver_path = os.environ.get("GECKODRIVER_PATH")
    if geckodriver_path:
        service = Service(executable_path=geckodriver_path)

    try:
        driver = webdriver.Firefox(service=service, options=options) if service else webdriver.Firefox(options=options)
    except Exception as e:
        log(f"[!] Error starting Firefox: {e}")
        sys.exit(1)

    driver.implicitly_wait(15)

    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}\n")
    log("[+] Starting (local, persistent profile)..." if not use_cookies else "[+] Starting (cookies)...")

    try:
        from keepstreak import keep_streak

        if use_cookies:
            if not load_cookies(driver):
                log("[!] Failed to load cookies.")
            elif is_logged_in(driver):
                log("[+] Session valid, running streak...")
                keep_streak(driver)
            else:
                log("[!] Not logged in. Re-export cookies and update THM_COOKIES_B64.")
        else:
            if is_logged_in(driver):
                log("[+] Session valid, running streak...")
                keep_streak(driver)
            else:
                log("[!] Not logged in. Run save_session.py again.")
    except Exception as e:
        log(f"[!] Fatal error: {e}")
    finally:
        log("[+] Closing...")
        driver.quit()


if __name__ == "__main__":
    main()
