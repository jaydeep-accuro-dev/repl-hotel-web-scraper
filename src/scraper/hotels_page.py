import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import CustomLogger

log = CustomLogger("hotels_page")


def load_hotels_page(driver, driver_timer, destination, check_in_date,
                     check_out_date):

    def _enter_destination():
        dest_input = WebDriverWait(driver=driver, timeout=driver_timer).until(
            EC.element_to_be_clickable((By.ID, "dest-input")))
        dest_input.send_keys(destination)
        dest_input.send_keys(Keys.RETURN)

    def _enter_dates():
        check_in_date_input = WebDriverWait(driver=driver,
                                            timeout=driver_timer).until(
                                                EC.element_to_be_clickable(
                                                    (By.ID, "checkInDate")))
        check_in_date_input.click()
        check_in_date_input.send_keys(check_in_date)
        check_in_date_input.send_keys(Keys.RETURN)

        check_out_date_input = WebDriverWait(driver=driver,
                                             timeout=driver_timer).until(
                                                 EC.element_to_be_clickable(
                                                     (By.ID, "checkInDate")))
        check_out_date_input.click()
        check_out_date_input.send_keys(check_out_date)
        check_out_date_input.send_keys(Keys.RETURN)

    def _search_hotels():
        search_button = WebDriverWait(driver=driver,
                                      timeout=driver_timer).until(
                                          EC.element_to_be_clickable(
                                              (By.CLASS_NAME,
                                               "search-button")))
        search_button.click()

    def _accept_cookies():
        accept_button = WebDriverWait(
            driver=driver, timeout=driver_timer
        ).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button[@id='truste-consent-button' and contains(text(), 'Continue')]",
            )))
        accept_button.click()

    try:
        _enter_destination()
        log.info("succeed to enter destination")
    except Exception as e:
        log.error("failed to enter destination")
        log.log_custom_exception(e, sys)

    try:
        _enter_dates()
        log.info("succeed to enter dates")
    except Exception as e:
        log.error("failed to enter dates")
        log.log_custom_exception(e, sys)

    try:
        _search_hotels()
        log.info("succeed to search hotels")
    except Exception as e:
        log.error("failed to search hotels")
        log.log_custom_exception(e, sys)

    time.sleep(5)
    log.info("wait for 5 seconds to load cookie button")

    try:
        _accept_cookies()
        log.info("succeed to click on cookie button")
    except Exception as e:
        log.error("failed to click on cookie button")
        log.log_custom_exception(e, sys)
