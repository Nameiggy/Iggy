import csv
def open_csv_file(filepath=str):
    with open(filepath,"r") as file:
        reader = csv.DictReader(file)
        return list(reader)