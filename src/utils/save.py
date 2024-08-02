import csv
import sys
from pathlib import Path
from src.utils.logger import CustomLogger
log = CustomLogger("save")

def save_to_csv(destination, file_name, hotel_data):
    try:
        if hotel_data:
            keys = hotel_data[0].keys()
            base_dir = Path(__file__).resolve().parent.parent.parent / destination
            base_dir.mkdir(parents=True, exist_ok=True)

            file_path = base_dir / file_name

            with file_path.open("w", newline="") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(hotel_data)
            
            log.info("succeed to save csv file")
    except Exception as e:
        log.error("failed to save csv file")
        log.log_custom_exception(e,sys)
            