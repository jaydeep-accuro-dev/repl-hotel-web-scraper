import sys
from pathlib import Path
from datetime import datetime, timedelta
src_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(src_path))
from main import scrape
from src.utils.logger import CustomLogger

if __name__ == "__main__":    
    destination = "Auburn, Alabama, United States"
    number_of_days = 1 
    unique_dates = [(datetime.now() + timedelta(days=i)).strftime("%d/%m/%Y") for i in range(number_of_days)]
    log = CustomLogger("Auburn_Alabama_United_States")
    log.info(f"scraper is running for {destination} : {unique_dates}")
    scrape(destination, number_of_days)
    log.info(f"scraper finished for {destination}")