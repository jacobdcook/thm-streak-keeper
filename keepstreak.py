import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

LOG = "tryhackmebot.log"


def out(msg):
    print(msg)
    with open(LOG, "a") as f:
        f.write(msg + "\n")


def keep_streak(driver):
    try:
        time.sleep(random.uniform(2, 4))
        driver.get("https://tryhackme.com/room/polkit")
        out("[+] Navigated to polkit room")

        reset_ok = False
        dropdown_selectors = [
            (By.CSS_SELECTOR, "button[aria-label='dropdown']"),
            (By.XPATH, "//button[contains(., 'Options')]"),
            (By.XPATH, "//div[contains(@class, 'dropdown')]"),
        ]
        for by, sel in dropdown_selectors:
            try:
                dropdown = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((by, sel))
                )
                dropdown.click()
                time.sleep(random.uniform(1, 2))
                reset_option = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Reset Progress')]"))
                )
                reset_option.click()
                time.sleep(random.uniform(1, 2))
                confirm = WebDriverWait(driver, 6).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, reset my progress')]"))
                )
                confirm.click()
                reset_ok = True
                out("[+] Reset progress clicked")
                break
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException):
                continue
        if not reset_ok:
            try:
                driver.find_element(By.XPATH, "//*[contains(text(), 'Reset')]").click()
                time.sleep(1)
                driver.find_element(By.XPATH, "//button[contains(text(), 'Yes')]").click()
                reset_ok = True
                out("[+] Reset (alt) clicked")
            except Exception:
                pass
        if not reset_ok:
            out("[!] Could not find Reset \u2013 page layout may have changed")

        time.sleep(random.uniform(1, 2))
        driver.get("https://tryhackme.com/room/polkit")
        time.sleep(random.uniform(2, 3))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(random.uniform(2, 3))

        complete_ok = False
        for xpath in [
            "//button[.//span[text()='Check']]",
            "//button[contains(., 'Check')]",
            "//button[@data-sentry-element='StyledButton' and contains(., 'Check')]",
            "//button[contains(text(), 'Complete')]",
            "//button[contains(text(), 'Submit')]",
        ]:
            try:
                btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                btn.click()
                complete_ok = True
                out("[+] Check / submit button clicked")
                break
            except (NoSuchElementException, TimeoutException):
                continue
        if not complete_ok:
            out("[!] Could not find Check/Complete/Submit \u2013 page layout may have changed")

        time.sleep(10)
        driver.get("https://tryhackme.com/room/polkit")
        time.sleep(8)

        try:
            streak_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='streak-trigger']"))
            )
            aria = streak_btn.get_attribute("aria-label")
            if aria and "day streak" in aria:
                streak = aria.replace(" day streak", "").strip()
            else:
                try:
                    streak = streak_btn.find_element(By.TAG_NAME, "p").text.strip()
                except Exception:
                    streak = streak_btn.text.strip() or "?"
            out(f"[+] Success! Your Streak is {streak}")
        except (NoSuchElementException, TimeoutException):
            try:
                el = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'streak')]")
                out(f"[+] Streak: {el.get_attribute('aria-label')}")
            except Exception:
                out("[!] Could not read streak counter \u2013 check tryhackme.com manually")
    except Exception as e:
        out(f"[!] keep_streak error: {e}")
        raise
