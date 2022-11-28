#!/usr/bin/env python3

from stricker_watcher import StrickerWatcher
from user_managment import ClientHandler,OsTools
from consol import Argument
import json
import os
from network_manager import NetworkManager
from time import sleep


class Config:
    def __init__(
        self,
        conf_dir:str
    )->None :

        self.conf_dir = conf_dir
        
        with open(self.conf_dir,"r") as f :
            self.conf_dict = json.loads(f.read()) 
            self.xray_conf = self.conf_dict["XRAY_CONF"]
            self.access_dir = self.conf_dict["ACCESS_DIR"]
            self.banning_on = self.conf_dict["BANNING_ON"]
            self.debug = self.conf_dict["DEBUG"]


class XrayHandler:
    def __init__(self):
        self.system_conf = Config("/root/Xray-ClientManager/conf.json")
        self.client_handler = ClientHandler(self.system_conf.xray_conf)
        self.arguments = Argument()
        # Configuration For Stricker Watcher
        self.watcher = StrickerWatcher(check_period=0,
            access_dir= self.system_conf.access_dir,
            bannig_on= self.system_conf.banning_on,
            debug= self.system_conf.debug
            )


    def consol_start(self):
        #Ceating Log Direcotry
        #self.creat_log_dir()
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
                    print("\r\n\r\n--------------------------------------------------Client VLESS URL-----------------------------------------------------------------")
                    url_vless = self.client_handler.get_client_url(email,domain,vpn_name)
                    print(url_vless)
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print("--------------------------------------------------Client VMESS URL-----------------------------------------------------------------")
                    url_vmess = self.client_handler.get_client_url_vmess(email,domain,vpn_name)
                    print(url_vmess)
                    print("----------------------------------------------------------------------------------------------------------------------------\r\n\r\n")
                    #self.client_handler.get_client_qrcode(email,url)
                    


            elif command == "add":
                raw_user: str=self.arguments.args.raw
                connection_profile: list = raw_user.split("@")
                if len(connection_profile) == 1 :
                    print("Error Please Insert The User Device Connectivity |x@|")
                    exit()
            
                self.client_handler.add_user(connection_profile[1],["vmess","vless"],connection_profile[0])
                # Here we Apply Changes if The Users specify it
                if self.arguments.args.apply :
                    self.client_handler.apply_changes()
                    

            elif command == "check":
                interval= self.arguments.args.wait
                # To make sure That the Time Has a deafault value
                if interval == None :
                    interval = 50 
                self.watcher.check_period = interval
                email_list = self.client_handler.get_clients_email_list()
                self.watcher.stanalone_stricker_watcher(email_list, self.client_handler)
            # here Parse The Command For Apply changes on Xray
            elif command == "apply" :
                self.client_handler.apply_changes()

            elif command == "unvalidate" : 
                email = self.arguments.args.email
                self.client_handler.unvalidate_user(email)
                self.client_handler.apply_changes()

            elif command == "validate":
                email = self.arguments.args.email
                self.client_handler.validate_user(email)
                self.client_handler.apply_changes()

            elif command == "del":
                # email = self.arguments.args.email
                # self.client_handler.del_user(email)
                # self.client_handler.apply_changes()
                self.client_handler._get_inbounds_type()

            elif command == "get-all" :
                if self.arguments.args.domain == None :
                    print("error : Please Enter The Domain name with |-i domain-name|")
                    exit()
                if self.arguments.args.name == None :
                    print("error : Please Enter The vpn name  with |-n vpn-name|")
                    exit()

                domain:str =  self.arguments.args.domain
                vpn_name:str =  self.arguments.args.name
                vpn_name = vpn_name.replace(" ","+")
                clients_email = self.client_handler.get_clients_email_list()
                for client_email in clients_email :
                    print(f"\r\n\r\n--------------------------------------------------{client_email}-----------------------------------------------------------------\r\n")
                    print("--------------------------------------------------Client VLESS URL-----------------------------------------------------------------")
                    url_vless = self.client_handler.get_client_url(client_email,domain,vpn_name)
                    print(url_vless)
                    print("----------------------------------------------------------------------------------------------------------------------------")
                    print("--------------------------------------------------Client VMESS URL-----------------------------------------------------------------")
                    url_vmess = self.client_handler.get_client_url_vmess(client_email,domain,vpn_name)
                    print(url_vmess)
                    print("----------------------------------------------------------------------------------------------------------------------------\r\n\r\n")

                    

                

                

            




def main():   
    consol = XrayHandler()
    consol.consol_start()
    
    

if __name__ == "__main__":
    main()
