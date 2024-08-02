import time
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils.logger import CustomLogger
log = CustomLogger("hotels_detail")

def get_hotel_data(driver, driver_timer, destination, check_in_date, check_out_date, available_hotels):
    def wait_for_element(by, value, visibility=False):
        wait_func = (
            EC.visibility_of_element_located
            if visibility
            else EC.presence_of_element_located
        )
        return WebDriverWait(driver, timeout=driver_timer).until(
            wait_func((by, value))
        )
        
    def wait_for_elements(by, value, visibility=False):
        wait_func = (
            EC.visibility_of_all_elements_located
            if visibility
            else EC.presence_of_all_elements_located
        )
        return WebDriverWait(driver, timeout=driver_timer).until(
            wait_func((by, value))
        )
    
    def get_room_webpage_elements(hotel_card):
        hotel_card.click()
        log.info("Clicked on hotel card to view details")
        time.sleep(3)
        try:
            hotel_name_element = wait_for_element(
                By.XPATH, '//*[@id="topOfPage"]/div[3]/app-hotel-info-v2/button'
            )
            room_name_elements = wait_for_elements(
                By.XPATH,
                '//div[@class="roomInfo"]//h2[contains(@class, "roomName")]',
                visibility=True,
            )
            price_elements = wait_for_elements(
                By.XPATH,
                '//div[contains(@class, "total-price")]/span[contains(@class, "cash")]',
                visibility=True,
            )

            if hotel_name_element and room_name_elements and price_elements:
                log.info("Successfully found hotel name, room names, and prices")
                return hotel_name_element, room_name_elements, price_elements
        except Exception as e:
            log.error("failed to scrape room page elements")
            log.log_custom_exception(e,sys)
        return False

    def fetch_room_webpage_data(hotel_card):
        if is_element_presence := get_room_webpage_elements(hotel_card):
            hotel_name_element, room_name_elements, price_elements = is_element_presence
        else:
            return False

        hotel_name = hotel_name_element.text.strip()
        room_types = [room.text for room in room_name_elements]
        prices = [price.text for price in price_elements]
        log.info(f"Scraped hotel: {hotel_name}, rooms: {room_types}, prices: {prices}")

        return hotel_name, room_types, prices
    
    hotel_data = []
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        log.info("Scrolled to top of the hotels page")
        time.sleep(2)
    except Exception as e:
        log.error("failed to scroll to top for hotels page")
        log.log_custom_exception(e,sys)

    try:
        for index in range(available_hotels):
            try:
                if index >= 9:
                    driver.execute_script(
                        "window.scrollTo(0, document.documentElement.scrollHeight);"
                    )
                    log.info("Scrolled to bottom of the hotels page")
                    time.sleep(2)
            except Exception as e:
                log.error("failed to scroll to bottom for hotels page")
                log.log_custom_exception(e,sys)

            try:
                hotel_cards = wait_for_elements(
                    By.XPATH, "//button[contains(text(), 'Select Hotel')]"
                )
                log.info(f"Loaded hotel cards, total cards found: {len(hotel_cards)}")
            except Exception as e:
                log.error("failed to load hotel cards")
                log.log_custom_exception(e,sys)

            try:
                hotel_card = hotel_cards[index]
                log.info(f"Selected hotel card at index: {index}")
            except Exception as e:
                log.error(
                    f"failed to select hotel cards, total hotel card {len(hotel_cards)}, index {index} , available hotels {available_hotels}"
                )
                log.log_custom_exception(e,sys)

            if not (
                is_fetch_successful := fetch_room_webpage_data(
                    hotel_card
                )
            ):
                log.error("fetch room webpage data unsuccessful")
                return hotel_data

            hotel_name, room_types, prices = is_fetch_successful
            hotel_data.extend(
                {
                    "Location": destination,
                    "Check-in Date": check_in_date,
                    "Check-out Date": check_out_date,
                    "Hotel Name": hotel_name,
                    "Room Type": room_type,
                    "Price": price,
                }
                for room_type, price in zip(room_types, prices)
            )
            driver.back()
            log.info("Navigated back to hotel list")
            time.sleep(3)
            
            driver.execute_script(
                "window.scrollTo(0, document.documentElement.scrollHeight);"
            )
        log.info("Scrolled to bottom of the page for next hotel")
        time.sleep(2)
    except Exception as e:
        log.error("failed to scrape hotel data")
        log.log_custom_exception(e, sys)

    log.info(f"Scraping completed, total hotels data collected: {len(hotel_data)}")
    return hotel_data