import random
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from human_behaviour import human_sleep, human_type
import config
import asyncio
import telegram
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

async def main():
    # Setup Firefox with options
    firefox_options = Options()
    firefox_options.set_preference("intl.accept_languages", "en-US, en")    # Language
    firefox_options.set_preference("dom.webdriver.enabled", False)          # Disables WebDriver flag
    firefox_options.set_preference("useAutomationExtension", False)         # Disables automation extension
    firefox_options.set_preference("media.navigator.enabled", False)        # Blocks camera/mic prompts
    firefox_options.set_preference("privacy.resistFingerprinting", True)    # Reduces fingerprinting
    firefox_options.set_preference("general.platform.override", "Win32")    # Mimics normal platform
    firefox_options.set_preference("dom.webnotifications.enabled", False)   # Disables web push popups
    firefox_options.set_preference("dom.webaudio.enabled", False)
    firefox_options.set_preference("media.peerconnection.enabled", False)
    firefox_options.set_preference("webgl.disabled", True)
    firefox_options.add_argument("--width=1280")
    firefox_options.add_argument("--height=800")


    #firefox_options.set_preference("useAutomationExtension", False)

    # Optional: Override user-agent to appear more human
    firefox_options.set_preference("general.useragent.override", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    # Initialize Firefox WebDriver
    driver = webdriver.Firefox(options=firefox_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    actions = ActionChains(driver)

    # Navigate to the login page
    human_sleep(2)
    driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4266647668&distance=25&f_WT=3%2C1&geoId=101100529&keywords=Sviluppatore%20back-end&origin=JOBS_HOME_SEARCH_CARDS&position=38&pageNum=0")

    try:
        alert = driver.switch_to.alert
        print("Dismissing unexpected alert:", alert.text)
        alert.dismiss()
    except:
        pass

    wait = WebDriverWait(driver, 10)
    
    print("Searching for modal...")
    # Wait for the modal with the right heading to appear
    modal = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'sign-in-modal')]//h2[contains(text(), 'Sign in to view more jobs')]")
    ))
    human_sleep(5)

    try:
        print("Searching for button...")
        # Once modal is found, find the button inside it
        # Wait until it's present (skip clickable here)
        wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//div[contains(@class, 'sign-in-modal')]//button[contains(@class, 'sign-in-modal__outlet-btn') and contains(., 'Sign in')]"
        )))
        print("Button found. Relocating...")
        # Then re-locate just before clicking
        sign_in_button = driver.find_element(By.XPATH,
            "//div[contains(@class, 'sign-in-modal')]//button[contains(@class, 'sign-in-modal__outlet-btn') and contains(., 'Sign in')]"
        )
    except:
        print("Button not found. Retrying...")
        sign_in_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class, 'sign-in-modal')]//button[contains(@class, 'sign-in-modal__outlet-btn') and contains(., 'Sign in')]"
        )))

    human_sleep(5)
    print("Clicking button...")
    # Scroll and click using JS to bypass hidden overlays
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sign_in_button)
    driver.execute_script("arguments[0].click();", sign_in_button)

    human_sleep(2)

    # Fill in username and password
    try:
        print("Filling credentials (1)...")
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "public_jobs_ai_button_contextual_sign_in_info_modal_sign-in-modal_session_key")))
        # Scroll it into view using JS
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_field)
        human_sleep(0.5)  # Slight pause to let things settle
        actions.move_to_element(username_field).pause(0.5).perform()
        username_field.click()
        human_type(username_field, config.username)
        human_sleep(2)
        password_field = driver.find_element(By.ID, "public_jobs_ai_button_contextual_sign_in_info_modal_sign-in-modal_session_password")
        # Scroll it into view using JS
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_field)
        human_sleep(0.5)  # Slight pause to let things settle
        actions.move_to_element(password_field).pause(0.5).perform()
        password_field.click()
        human_type(password_field, config.password)
        password_field.send_keys(Keys.RETURN)
    except:
        print("Filling credentials (2)...")
        username_field = wait.until(EC.visibility_of_element_located((By.ID, "base-sign-in-modal_session_key")))
        # Scroll it into view using JS
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_field)
        human_sleep(0.5)  # Slight pause to let things settle
        actions.move_to_element(username_field).pause(0.5).perform()
        username_field.click()
        human_type(username_field, config.username)
        human_sleep(2)
        password_field = driver.find_element(By.ID, "base-sign-in-modal_session_password")
        # Scroll it into view using JS
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", password_field)
        human_sleep(0.5)  # Slight pause to let things settle
        actions.move_to_element(password_field).pause(0.5).perform()
        password_field.click()
        human_type(password_field, config.password)
        password_field.send_keys(Keys.RETURN)
    
    #driver.quit()

if __name__=="__main__":
    asyncio.run(main())
