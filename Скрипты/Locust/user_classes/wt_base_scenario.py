from locust import task, SequentialTaskSet, FastHttpUser, HttpUser, constant_pacing, events
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file,generateFlightsDates,generateRandomCardNumber
import sys,re,random
from urllib.parse import quote_plus

class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)


    test_users_csv_filepath = './test_data/test_users.csv'
    test_flights_data_csv_filepath='./test_data/data_users.csv'
    test_flights_data = open_csv_file(test_flights_data_csv_filepath)
    test_users_data = open_csv_file(test_users_csv_filepath)
    post_request_content_type={
            'Content-Type':'application/x-www-form-urlencoded'
        }

    def on_start(self):
        @task
        def uc_00_getHomePage(self) -> None:
    
            logger.info(f"Test data for user is:{self.test_users_data}")


            r00_0_headers = { 
                'sec-fetch-mode': 'navigate'
            }

            r00_0_response = self.client.get(
                f'/WebTours/',
                name="REQ_00_0_/WebTours/",
                allow_redirects=False,
                debug_stream=sys.stderr
            )


            r00_01_response = self.client.get(
                f'/WebTours/header.html',
                name="REQ_00_1_getHomePage/WebTours/header.html",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )

            ur1_param_signOff = 'true'

            r00_02_response = self.client.get(
                '/cgi-bin/welcome.pl?signOff=true',
                name="REQ_00_2_getHomePage_cgi-bin/welcome.pl?signOff=true",
                allow_redirects=False,
                debug_stream=sys.stderr
            )
            
            with self.client.get(
                f'/cgi-bin/nav.pl?in=home',
                name="REQ_00_3_getHomePage_cgi-bin/nav.pl?in=home",
                allow_redirects=False,
                catch_response=True,
                #debug_stream=sys.stderr
            )as req00_03_response: 
                check_http_response(req00_03_response,'name="userSession"') 
                #print(f"\n___\n req_00_3 response text:{r00_03_response.text}\n___\n")
                
        
            self.user_session = re.search(r"name=\"userSession\" value=\"(.*)\"\/>",req00_03_response.text).group(1)

            
            # logger.info(f"r00_03_response_text:{req00_03_response.text}")
            logger.info(f"user_session:{self.user_session}")



        
            r00_04_response = self.client.get(
            f'/WebTours/home.html',
                name="REQ_00_4_getHomePage_WebTours/home.html",
                allow_redirects=False,
                #debug_stream=sys.stderr
            )
        @task
        def uc_00_LoginAction(self) -> None:
            self.users_data_row = random.choice(self.test_users_data)
            logger.info(self.users_data_row)   

            self.username = self.users_data_row["Login"]
            self.password = self.users_data_row["password"]
            self.firstName = self.users_data_row["firstName"]
            self.lastName = self.users_data_row["lastName"]
            self.address1 = self.users_data_row["address1"]
            self.address2 = self.users_data_row["address2"]
            self.pass1 = self.users_data_row["pass1"]

            logger.info(f"chosen username:{self.username}password:{self.password}")

            r_01_00_body = f"userSession={self.user_session}&username={self.username}&password={self.password}&login.x=58&login.y=4&JSFormSubmit=off"

            with self.client.post(
                f'/cgi-bin/login.pl',
                 name='req_01_0_LoginAction/cgi-bin/login.pl',
                 headers=self.post_request_content_type,
                 data=r_01_00_body,
                 #debug_stream=sys.stderr,
                 catch_response=True,

            )as r_01_00_response: 
                check_http_response(r_01_00_response,"User password was correct")

            with self.client.get(
                f'/cgi-bin/nav.pl?page=menu&in=home',
                name = "req_01_01_LoginAction_/cgi-bin/nav.pl?page=menu&in=home",
                debug_stream=sys.stderr,
                catch_response=True
            ) as r_01_01_response:
                check_http_response(r_01_01_response,"Web Tours Navigation Run")

            with self.client.get(
                f'/cgi-bin/login.pl?intro=true',
                name='req_01_02_LoginAction_/cgi-bin/login.pl?intro=true',
                #debug_stream=sys.stderr,
                catch_response=True
            ) as r_01_02_response:
                check_http_response(r_01_02_response,"Welcome to Web Tours")   

           

        uc_00_getHomePage(self)
        uc_00_LoginAction(self)       
    @task
    def uc02_OpenFlightsTab(self):
        self.client.get(
            f'/cgi-bin/welcome.pl?page=search',
            name = "req_02_0_OpenFlightsTab_cgi-bin/welcome.pl?page=search",
            allow_redirects=False,
           # debug_stream=sys.stderr
        )

        self.client.get(
            f'/cgi-bin/nav.pl?page=menu&in=flights',
            name = "req_02_1_OpenFlightsTab_cgi-bin/nav.pl?page=menu&in=flights",
            allow_redirects=False,
            #debug_stream=sys.stderr
        )

        self.client.get(
            f'/cgi-bin/reservations.pl?page=welcome',
            name = "req_02_2_OpenFlightsTab_cgi-bin/reservations.pl?page=welcome",
            allow_redirects=False,
           # debug_stream=sys.stderr
        )
    @task
    def uc03_FindFlight_InputParams(self):
        self.test_flights_data_row = random.choice(self.test_flights_data)

        depart = self.users_data_row["depart"]
        arrive = self.users_data_row["arrive"]
        self.seatPref= self.test_flights_data_row["seatPref"]
        self.seatType= self.test_flights_data_row["seatType"]
        self.expDate = self.test_flights_data_row["expDate"]

        dates_dict = generateFlightsDates()

    
        r03_00_body = f"advanceDiscount=0&depart={depart}&departDate={dates_dict["depart_Date"]}&arrive={arrive}&returnDate={dates_dict["return_Date"]}&numPassengers=1&seatPref={self.seatPref}&seatType={self.seatType}&findFlights.x=54&findFlights.y=10&.cgifields=roundtrip&.cgifields=seatType&.cgifields=seatPref"
        logger.info(f"uc03_request body: {r03_00_body}")


        with self.client.post(
            f'/cgi-bin/reservations.pl',
            name='req_03_0_FindFlight_InputParams_/cgi-bin/reservations.pl',
            headers=self.post_request_content_type,
            data=r03_00_body,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r_03_0_response:
            pass
            check_http_response(r_03_0_response, "Flight departing from") 
            self.outboundFlight = re.search(r" name=\"outboundFlight\" value=\"(.*)\">", r_03_0_response.text).group(1)

    @task
    def uc04_ChooseFightOption(self):
        
        r04_00_body = f"outboundFlight={quote_plus(self.outboundFlight)}&numPassengers=1&advanceDiscount=0&seatType={self.seatType}&seatPref={self.seatPref}&reserveFlights.x=52&reserveFlights.y=11"
        logger.info(f"uc04_request body: {r04_00_body}")


        with self.client.post(
            f'/cgi-bin/reservations.pl',
            name='req_04_0_ChooseFightOption_/cgi-bin/reservations.pl',
            headers=self.post_request_content_type,
            data=r04_00_body,
           # debug_stream=sys.stderr,
            catch_response=True
        ) as r_04_0_response:
            pass
            check_http_response(r_04_0_response,"Total for 1 ticket(s) is =") 
    @task
    def uc05_ConfirmFlightBooking(self):
        
        r05_00_body = f"firstName={self.firstName}&lastName={self.lastName}&address1={quote_plus(self.address1)}&address2={quote_plus(self.address2)}&pass1={quote_plus(self.firstName + ' ' + self.lastName)}&creditCard={generateRandomCardNumber()}&expDate={quote_plus(self.expDate)}&saveCC=on&oldCCOption=on&numPassengers=1&seatType={self.seatType}&seatPref={self.seatPref}&outboundFlight={quote_plus(self.outboundFlight)}&advanceDiscount=0&returnFlight=&JSFormSubmit=off&buyFlights.x=48&buyFlights.y=11&.cgifields=saveCC"
        logger.info(f"uc04_request body: {r05_00_body}")


        with self.client.post(
            f'/cgi-bin/reservations.pl',
            name='req_05_0_ConfirmFlightBooking_/cgi-bin/reservations.pl',
            headers=self.post_request_content_type,
            data=r05_00_body,
            debug_stream=sys.stderr,
            catch_response=True
        ) as r_05_0_response:
            pass
            #check_http_response(r_05_0_response,"Total for 1 ticket(s) is =")
    
        
    
class  WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста:
     wait_time = constant_pacing(cfg.webtours_base.pacing)

     host = cfg.url
     logger.info(f'WebToursBaseUserClass started. Host: {host}')
     tasks = [PurchaseFlightTicket]