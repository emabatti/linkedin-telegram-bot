from bs4 import BeautifulSoup
from requests_html import HTMLSession
import config
import asyncio
import telegram
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # Firefox options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException

class Job:
    title: str
    company: str
    time_ago: str
    link: str


async def old_main():
    bot = telegram.Bot(config.api_token) 
    session = HTMLSession()
     
    async def send_message(job: Job = Job()):
        text = f'<b><a href="{job.link}">{job.title}</a></b>'
        await bot.send_message(text=text, chat_id=config.chat_id, parse_mode="HTML")
    
    # preparing driver to allow for js loading before parsing the page
    while True:
        jobs = []
        for url in config.urls:
            page = session.get(url)
            soup = BeautifulSoup(page.text,"lxml")

            listings = soup.select('#main-content section > ul li')

            if listings:
                for listing in listings:
                    job = Job()
                    job.title = listing.h3.string.strip()
                    job.company = listing.h4.a.string.strip()
                    job.time_ago = listing.time.string.strip()
                    job.link = listing.a['href'].strip()
                    jobs.append(job)
                
        for job in jobs:
            await send_message(job)
        time.sleep(config.seconds)

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

    # Optional: Override user-agent to appear more human
    firefox_options.set_preference("general.useragent.override", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
        "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    # Initialize Firefox WebDriver
    driver = webdriver.Firefox(options=firefox_options)

    # Navigate to the login page
    driver.get("https://www.linkedin.com/jobs")

    try:
        alert = driver.switch_to.alert
        print("Dismissing unexpected alert:", alert.text)
        alert.dismiss()
    except:
        pass

    wait = WebDriverWait(driver, 20)
    
    print("Searching for modal...")
    # Wait for the modal with the right heading to appear
    modal = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'sign-in-modal')]//h2[contains(text(), 'Sign in to view more jobs')]")
    ))

    try:
        print("Searching for button...")
        # Once modal is found, find the button inside it
        sign_in_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class, 'sign-in-modal')]//button[contains(@class, 'sign-in-modal__outlet-btn') and contains(., 'Sign in')]"
        )))
    except:
        print("Button not found. Retrying...")
        # Once modal is found, find the button inside it
        sign_in_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class, 'sign-in-modal')]//button[contains(@class, 'sign-in-modal__outlet-btn') and contains(., 'Sign in')]"
        )))

    time.sleep(5)
    print("Clicking button...")     
    driver.execute_script("arguments[0].click();", sign_in_button)

    # Fill in username and password
    username_field = wait.until(EC.presence_of_element_located((By.ID, "base-sign-in-modal_session_key")))
    username_field.clear()
    username_field.send_keys("your_username")

    time.sleep(2)

    password_field = driver.find_element(By.ID, "base-sign-in-modal_session_password")
    password_field.clear()
    password_field.send_keys("your_password")

if __name__=="__main__":
    asyncio.run(main())
