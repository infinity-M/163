# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00DE12CE348AB6353F317BF52531333646DD856EE8BC85E50E4EC556F11443F4F51EB08F92EA4CC50D2C783737771E811C056B88B76E5C8BD5A4DBEE3BEBF31AF500D9C971918EEF7A2C687881FE8590DE36CCDF598ABE21E7BC708B28C4B962A13A9384B286534EA25BF12D112A1FFE6EC4D9CACCB0601DE7835DC3B7D065503CE3AE2AC9AAB5CBE3CE08DF9FCED9AE491C2F8393B97CBE1ADFF6CA1B8D6A2AFDA0CB08238F85A14370CB22461ED70FDA0EDFB725DF4AAFBD3838196CA8D044E4226A0FD9DED7DDB8E0A4BBC756453904EABD9F93BCD368CE9271E5D183B37FE9BD178F2B0B8825E01622BA9234DFE2DEAC4B1769D5070B88A6F0881B0376BE97A968CE94EE7925A8009346EA99B97657D40AF1CE77208B3C4EDE2CA9B1AA3B0C96A6CE3BA328D2BDD11EC62E1D858A10C07AB744713F770D3B53EE4A69A8719FF7D7D70E3BA88E3AA3A8C59466A920AE9EE7CB99E19CB43123FC766AFFDE63A84E654C873EC97F9FFBE583F0CF6903121F430DFBB5B14F7E31F35A1C72B0DA2193C6B5C26FA0D6BF3CB4212DC8D427EC"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
