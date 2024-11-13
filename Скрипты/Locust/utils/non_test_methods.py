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

def processCancelReqvestBody(ids_list=list, names_list=list):

 
    flight_part = "flightID="+"&flightID=".join(ids_list)

    cgi_part = ".cgifields="+"&.cgifields=".join(names_list)

    todelete_part = f"{names_list[random.randrange(0,len(ids_list))]}=on"

    static_part = "&removeFlights.x=43&removeFlights.y=10"

    result = f"{todelete_part}&{flight_part}&{cgi_part}&{static_part}"
    return result



