import random
from datetime import datetime,timedelta
from urllib.parse import quote_plus

n = 0
while n < 10:
    #print(random.randrange(1,5))
    #side_date = datetime.now() + timedelta(days=random.randint(1,10))
    #another_side_date = datetime.now() + timedelta(days=random.randint(15,30))
    #n += 1

    #print(f"my generated dates: {side_date.strftime("%m/%d/%Y")} : {another_side_date.strftime("%m/%d/%Y")}\n_________")
    #print(f"my generated dates: {quote_plus(side_date.strftime("%m/%d/%Y"))} : {quote_plus(another_side_date.strftime("%m/%d/%Y"))}")


    print(random.randrange(10**15,10**16)) 
    n+=1  