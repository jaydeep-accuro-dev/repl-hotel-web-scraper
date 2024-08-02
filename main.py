from src.utils import logger, driver, date_pairs, file, save
from src.scraper import hotels_page, hotels_count, hotels_detail

log = logger.CustomLogger("main")


def scrape(destination, number_of_days):
    url = "https://www.ihg.com/hotels/us/en/reservation"
    dates = date_pairs.create_date_pairs(number_of_days)
    timer = 120

    for check_in_date, check_out_date in dates:
        chrome_driver = driver.get_driver(url)
        hotels_page.load_hotels_page(chrome_driver, timer, destination,
                                     check_in_date, check_out_date)
        hotels_count.get_total_hotels_count(chrome_driver, timer)
        available_hotels = hotels_count.get_available_hotels_count(
            chrome_driver, timer)
        hotel_data = hotels_detail.get_hotel_data(chrome_driver, timer,
                                                  destination, check_in_date,
                                                  check_out_date,
                                                  available_hotels)
        file_name = file.generate_file_name(destination, check_in_date,
                                            check_out_date)
        save.save_to_csv(destination, file_name, hotel_data)
        chrome_driver.quit()
        log.info("succeed to quit driver")
