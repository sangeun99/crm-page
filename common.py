import csv

def get_data_from_file(filename):
    data = []
    with open(filename, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        next(reader)
        for row in reader:
            data.append(row)
    return data

def get_pages_indexes(data_length, page):
    per_page = 20
    total_pages = (data_length - 1) // per_page + 1
    start_index = (page - 1) * per_page
    end_index = page * per_page
    return total_pages, start_index, end_index
