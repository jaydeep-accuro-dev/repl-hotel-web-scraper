import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import CustomLogger
log = CustomLogger("hotels_count")


def get_total_hotels_count(driver, driver_timer):
    try:
        hotel_count_element = WebDriverWait(
            driver=driver, timeout=driver_timer
        ).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//div[contains(@class, "rooms-count-container")]/div[contains(@class, "rooms-count")]/div',
                )
            )
        )
        hotel_count = int(hotel_count_element.text.split()[0])
        log.info(f"succeed to calculate total hotels {hotel_count}")
        return hotel_count
    except Exception as e:
        log.error("failed to calculate total hotels")
        log.log_custom_exception(e,sys)

def get_available_hotels_count(driver, driver_timer):
    try:
        hotel_count = 0

        for _ in range(3):
            scroll_amount = (
                driver.execute_script(
                    "return document.documentElement.scrollHeight"
                )
                / 2
            )
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

            time.sleep(3)

            hotel_elements = WebDriverWait(driver, driver_timer).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[contains(text(), 'Select Hotel')]")
                )
            )

            hotel_count = max(hotel_count, len(hotel_elements))

        log.info(f"succeed to calculate available hotels {hotel_count}")
        return hotel_count
    except Exception as e:
        log.error("failed to calculate available hotels")
        log.log_custom_exception(e,sys)
