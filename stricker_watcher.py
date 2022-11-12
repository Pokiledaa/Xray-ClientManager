import time
from re import search
# ACCESS_LOG_DIR = ""



class StrickerWatcher:
    def __init__ (
        self,
        check_period,
    ):
        # how often The Watcher Should Loock after strickers
        self.check_period = check_period
        


    def reading_client_logs (self) ->list:
       
        fd = open("access.log","r") 
        # for counter in range(100):
        lines: list = fd.read().splitlines()
        fd.close()
        return lines

    def count_ip_per_user(self,emails: list):
        # this The Total Connect
        total_current_conn: int = 0
        total_max_conn:int = 0
        # the main Stricker List List That Contains The Stricker Profiles as Chiled
        stricker_list: list = []

        for email in emails:
            # appendinf $ in the end of the email to tell what phrase to lock after
            # Empty Stricker Profile For Getting Empty in every loop
            stricker_profile: dict = {}
            
            # Here We Calculate The User Max Device Connection
            parsed_client: list = email.split("@")
            client_max_conn = int(parsed_client[0])
            # Here we Calcultate The User Max Client
            total_max_conn += client_max_conn 
            # Here We Read The Client Logs
            lines = self.reading_client_logs()
            client_ip_list:list = []
            for line in lines :
                if isinstance(line,str) :
                    if search(email+"$",line):
                        
                        sub_line: list = line.split(" ")
                        client_ip_list.append(sub_line[2])
                        
            client_unique_ip: set = set(client_ip_list)
            client_unique_ip_count = len(client_unique_ip)
            # Here We Calculate Total Current Connection
            total_current_conn += client_unique_ip_count
            if client_unique_ip_count > client_max_conn :
                stricker_profile = {
                    "email":email,
                    "max_conn": client_max_conn,
                    "current_conn": client_unique_ip_count
                }
                stricker_list.append(stricker_profile)

        connection_status = {
            "current_connection": total_current_conn,
            "max_connection": total_max_conn
        }
       
        return (stricker_list , connection_status)

    
    def stanalone_stricker_watcher(self, emails:list ):


        while True:

            time.sleep(self.check_period)

            striker_list , connection = self.count_ip_per_user(emails)
            curr_conn = connection["current_connection"]
            max_conn = connection["max_connection"]

            for stricker in striker_list:
                print(f"Stricker : \r\n{stricker}")
                
            print(f"Connection Status : {curr_conn}/{max_conn}")
        

        

                    

        # for email in emails:
        #     for line in lines:
        #         splited_line=line.split(" ")


    def _find_ip_per_user(self, line: str) :
        pass

                
            
        



    

            

