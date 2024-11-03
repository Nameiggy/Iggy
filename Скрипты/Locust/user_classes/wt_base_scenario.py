from locust import task, SequentialTaskSet, FastHttpUser, HttpUser, constant_pacing, events
from config.config import cfg, logger
from utils.assertion import check_http_response
from utils.non_test_methods import open_csv_file
import sys,re,random

class PurchaseFlightTicket(SequentialTaskSet): # класс с задачами (содержит основной сценарий)


    test_users_csv_filepath = './test_data/test_users.csv'

    def on_start(self):
        @task
        def uc_00_getHomePage(self) -> None:
            self.test_users_data = open_csv_file(self.test_users_csv_filepath)
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
            r01_00_headers={
                'content-type': 'application/x-www-form-urlencoded'

            }
            self.users_data_row = random.choice(self.test_users_data)
            logger.info(self.users_data_row)   

            self.username = self.users_data_row["Login"]
            self.password = self.users_data_row["password"]

            logger.info(f"chosen username:{self.username}/password:{self.password}")

            r_01_00_body = f"userSession={self.user_session}&username={self.username}&password={self.password}&login.x=58&login.y=4&JSFormSubmit=off"

            with self.client.post(
                f'/cgi-bin/login.pl',
                 name='req_01_0_LoginAction/cgi-bin/login.pl',
                 headers=r01_00_headers,
                 data=r_01_00_body,
                 debug_stream=sys.stderr,
                 catch_response=True,

            )as r_01_00_response: 
                check_http_response(r_01_00_response,"User password was correct")

            with self.client.get(
                f'/cgi-bin/nav.pl?page=menu&in=home',
                name = 'req_01_01_LoginAction_/cgi-bin/nav.pl?page=menu&in=home',
                debug_stream=sys.stderr,
                catch_response=True
            ) as r_01_01_response:
                check_http_response(r_01_01_response,"Web Tours Navigation Run")

            with self.client.get(
                f'/cgi-bin/login.pl?intro=true',
                name='req_01_02_LoginAction_/cgi-bin/login.pl?intro=true',
                debug_stream=sys.stderr,
                catch_response=True
            ) as r_01_02_response:
                check_http_response(r_01_02_response,"Welcome to Web Tours")   

           

        uc_00_getHomePage(self)
        uc_00_LoginAction(self)       
    @task
    def mydumy_task(self):
        print("chto-to")       

            
        
    
class  WebToursBaseUserClass(FastHttpUser): # юзер-класс, принимающий в себя основные параметры теста:
     wait_time = constant_pacing(cfg.pacing)

     host = cfg.url
     logger.info(f'WebToursBaseUserClass started. Host: {host}')
     tasks = [PurchaseFlightTicket]