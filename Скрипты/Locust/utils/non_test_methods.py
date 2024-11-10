import csv,random
from datetime import datetime, timedelta
from urllib.parse import quote_plus
def open_csv_file(filepath=str):
    with open(filepath,"r") as file:
        reader = csv.DictReader(file)
        return list(reader)


def generateFlightsDates():
    dates_list= {}
    dates_list["depart_Date"] = quote_plus((datetime.now() + timedelta(days=random.randint(3,10))).strftime("%m/%d/%Y"))
    dates_list["return_Date"] = quote_plus((datetime.now() + timedelta(days=random.randint(15,30))).strftime("%m/%d/%Y"))
    return dates_list

def generateRandomCardNumber():
    return random.randrange(10**15,10**16)

