#!/usr/bin/env python3

from stricker_watcher import StrickerWatcher
from user_managment import ClientHandler
from consol import Argument
import json


class Config:
    def __init__(
        self,
        conf_dir:str
    )->None :

        self.conf_dir = conf_dir
        
        self.conf_file = open(self.conf_dir,"r")
        self.conf_dict = json.loads(self.conf_file.read()) 
        self.xray_conf = self.conf_dict["XRAY_CONF"]

        self.conf_file.close()


class XrayHandler:
    def __init__(self):
        self.system_conf = Config("conf.json")
        self.client_handler = ClientHandler(self.system_conf.xray_conf)
        self.arguments = Argument()


    def consol_start(self):
        self.arguments.start()
        # Here we Parse The Get User
        if self.arguments.args.command :
            command = self.arguments.args.command

            if command == "get":
                if self.arguments.args.domain == None :
                    print("error : Please Enter The Domain name with |-i domain-name|")
                    exit()
                if self.arguments.args.name == None :
                    print("error : Please Enter The vpn name  with |-n vpn-name|")
                    exit()

                email:str = self.arguments.args.email
                domain:str =  self.arguments.args.domain
                vpn_name:str =  self.arguments.args.name
                vpn_name = vpn_name.replace(" ","+")
                profile = self.client_handler.get_client_profile(email)
                if not profile :
                    print("Error : No user Found")
                else : 
                    print("\r\n\r\n--------------------------------------------------Client URL-----------------------------------------------------------------")
                    url = self.client_handler.get_client_url(email,domain,vpn_name)
                    print(url)
                    print("----------------------------------------------------------------------------------------------------------------------------\r\n\r\n")
                    self.client_handler.get_client_qrcode(email,url)
                    


            elif command == "add":
                raw_user: str=self.arguments.args.raw
                connection_profile: list = raw_user.split("@")
                profile = connection_profile[1].split("-")
                if len(profile) != 5:
                    print("Error Please Insert The User Correctly")
                    exit()
                else :
                    self.client_handler.add_user(connection_profile[0],profile[0],profile[1]+" "+profile[2],profile[3],profile[4])
                    
                
            




def main():    
    consol = XrayHandler()
    consol.consol_start()
    # conf = Config("conf.json")
    # client = ClientHandler(conf.xray_conf)
    # client.add_user(2,9122237423,"parsa oskouie", "1401/8/7",1)
    

if __name__ == "__main__":
    main()
