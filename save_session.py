"""
Open TryHackMe in Firefox with a persistent profile.
Log in manually. Type 'done' when finished. Session persists for future runs.
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(SCRIPT_DIR, "firefox_thm_profile")


def main():
    os.chdir(SCRIPT_DIR)
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)

    options = Options()
    options.add_argument("-profile")
    options.add_argument(PROFILE_DIR)
    options.set_preference("dom.webnotifications.enabled", False)

    try:
        driver = webdriver.Firefox(options=options)
    except Exception as e:
        print(f"[!] Error starting Firefox: {e}")
        sys.exit(1)

    driver.get("https://tryhackme.com/login")
    print("\n  Log in to TryHackMe in the browser window.")
    print("  When you're logged in and see your dashboard, come back here.")
    print("  Type  done  and press Enter.\n")

    while True:
        try:
            line = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if line == "done":
            break
        print('  Type "done" when you have finished logging in.')

    driver.quit()
    print(f"[+] Session saved in {PROFILE_DIR}")
    print("  Run the streak bot or set up cron.\n")


if __name__ == "__main__":
    main()
