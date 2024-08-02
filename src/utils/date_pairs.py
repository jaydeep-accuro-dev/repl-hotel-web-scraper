from datetime import datetime, timedelta
from src.utils.logger import CustomLogger

def create_date_pairs(number_of_days):
    log = CustomLogger("date_pairs")
    num_dates = number_of_days + 1
    start_date = datetime.now()
    dates = [start_date + timedelta(days=i) for i in range(num_dates)]
    date_pairs = list(zip(dates[:-1], dates[1:]))
    date_pairs = tuple(
        (date1.strftime("%d/%m/%Y"), date2.strftime("%d/%m/%Y"))
        for date1, date2 in date_pairs
    )
    log.info(f"succeed to create date pairs {date_pairs}")
    return date_pairs