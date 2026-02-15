"""
Export TryHackMe session cookies for GitHub Actions (small secret, fits in 64KB).
Run after save_session.py. Creates thm_cookies.json; base64 that file for THM_COOKIES_B64.
"""
import json
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(SCRIPT_DIR, "firefox_thm_profile")
COOKIES_FILE = os.path.join(SCRIPT_DIR, "thm_cookies.json")


def main():
    os.chdir(SCRIPT_DIR)
    if not os.path.exists(PROFILE_DIR):
        print("[!] No firefox_thm_profile. Run save_session.py first, log in, type done.")
        sys.exit(1)

    options = Options()
    options.add_argument("-profile")
    options.add_argument(PROFILE_DIR)
    options.set_preference("dom.webnotifications.enabled", False)

    try:
        driver = webdriver.Firefox(options=options)
    except Exception as e:
        print(f"[!] Error starting Firefox: {e}")
        sys.exit(1)

    driver.get("https://tryhackme.com")
    driver.implicitly_wait(5)
    cookies = driver.get_cookies()
    driver.quit()

    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"[+] Saved {len(cookies)} cookies to {COOKIES_FILE}")
    print("    For GitHub Actions: base64 -w0 thm_cookies.json > cookies.b64")
    print("    Then add secret THM_COOKIES_B64 with the contents of cookies.b64")


if __name__ == "__main__":
    main()
