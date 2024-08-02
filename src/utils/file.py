def generate_file_name(destination, check_in_date, check_out_date):
    formatted_destination = destination.replace(", ", "_").replace(" ", "_")
    formatted_check_in = check_in_date.replace("/", "_")
    formatted_check_out = check_out_date.replace("/", "_")
    return (
        f"{formatted_destination}_{formatted_check_in}_To_{formatted_check_out}.csv"
    )