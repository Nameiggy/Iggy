from locust import task, SequentialTaskSet, FastHttpUser, HttpUser, constant_pacing, events
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import processCancelReqvestBody, open_csv_file
import sys, re, random
from urllib.parse import quote_plus



class CanchelFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)

    test_users_csv_filepath = './test_data/test_users.csv'
    test_flights_data_csv_filepath='./test_data/data_users.csv'
    test_flights_data = open_csv_file(test_flights_data_csv_filepath)
    test_users_data = open_csv_file(test_users_csv_filepath)
    
 

    post_request_content_type = {
        'Content-Type': 'application/x-www-form-urlencoded'
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
                #debug_stream=sys.stderr
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
                #debug_stream=sys.stderr
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
            
            #self.username ="mark"
            #self.password ="tven"

            logger.info(f"chosen username:{self.username}password:{self.password}")

            r_01_00_body = f"userSession={self.user_session}&username={self.username}&password={self.password}&login.x=58&login.y=4&JSFormSubmit=off"

            with self.client.post(
                f'/cgi-bin/login.pl',
                 name='req_01_0_LoginAction/cgi-bin/login.pl',
                 headers=self.post_request_content_type,
                 data=r_01_00_body,
                 #debug_stream=sys.stderr,
                 catch_response=True

            )as r_01_00_response: 
                check_http_response(r_01_00_response,"User password was correct")

            with self.client.get(
                f'/cgi-bin/nav.pl?page=menu&in=home',
                name = "req_01_01_LoginAction_/cgi-bin/nav.pl?page=menu&in=home",
                #debug_stream=sys.stderr,
                catch_response=True
            ) as r_01_01_response:
                check_http_response(r_01_01_response,"Web Tours Navigation Bar")

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
    def uc06_OpenBookedFlightsTab(self):
       self.client.get(
            f'/cgi-bin/welcome.pl?page=itinerary',
            name = "req_06_0_OpenBookedFlightsTab_cgi-bin/welcome.pl?page=itinerary",
            allow_redirects=False,
            #debug_stream=sys.stderr

       )



       self.client.get(
            f'/cgi-bin/nav.pl?page=menu&in=itinerary',
            name = "req_06_1_OpenBookedFlightsTab_cgi-bin/nav.pl?page=menu&in=itinerary",
            allow_redirects=False,
            #debug_stream=sys.stderr

       )


       with self.client.get(
            f'/cgi-bin/itinerary.pl',
            name = "req_06_2_OpenBookedFlightsTab_cgi-bin/itinerary.pl",
            allow_redirects=False,
            #debug_stream=sys.stderr
       ) as response_06_2:
           check_http_response(response_06_2, "Flights List") 

           self.fiyght_ids = re.findall(r'<input type=\"hidden\" name=\"flightID\" value=\"(.*)\"', response_06_2.text)
           self.fiyght_names = re.findall(r'<input type=\"hidden\" name=\"\.cgifields\" value=\"([0-9]{1,4})\"', response_06_2.text)

           logger.info(f"self.fiyght_ids;{self.fiyght_ids}")
           logger.info(f"self.fiyght_names;{self.fiyght_names}")


       


    @task
    def uc07_ChancelOneTicket(self):
            if self.fiyght_ids:
                logger.info('THERE ARE 1 OR MORE TICKETS!')
                req_07_0_body = processCancelReqvestBody(self.fiyght_ids,self.fiyght_names )
                logger.info(f"req_07_0_body: {req_07_0_body}")

                with self.client.post(
                '/cgi-bin/itinerary.pl',
            name='req_07_0_ChancelOneTicket_cgi-bin/itinerary.pl',
            headers=self.post_request_content_type,
            data=req_07_0_body,
            debug_stream=sys.stderr,
            catch_response=True

            ) as req_07_00response:
                    pass
                check_http_response(req_07_00response, "Flights List") 
            else:
                logger.info('THERE ARE NO TICKETS FOR TEST USER')   
            
            

           
            

            
        

class  WebToursCancelUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста:_
     wait_time = constant_pacing(cfg.webtours_cancel.pacing)

     host = cfg.url
     logger.info(f'WebToursCancelUserClass started. Host: {host}')
     tasks = [CanchelFlightTicket]
