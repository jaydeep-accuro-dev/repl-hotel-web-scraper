import time
import sys
from selenium.webdriver import Chrome, ChromeOptions
from src.utils.logger import CustomLogger

log = CustomLogger("driver")


def get_options():
    options = ChromeOptions()

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extentsions")
    options.add_argument("--disable-infobars")
    # options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    return options


def get_driver(url):
    try:
        options = get_options()
        chrome_driver = Chrome(options=options)
        chrome_driver.get(url)
        chrome_driver.maximize_window()
        time.sleep(3)
        log.info("succeed to load driver")
        return chrome_driver
    except Exception as e:
        log.error("failed to load driver")
        log.log_custom_exception(str(e), sys)
