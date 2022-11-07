
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

    def count_ip_per_user(self,emails):
        lines = self.reading_client_logs()
        for email in emails:
            for line in lines:
                splited_line=line.split(" ")
                
            
        



    

            

