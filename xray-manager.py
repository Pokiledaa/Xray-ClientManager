#!/usr/bin/env python3

from stricker_watcher import StrickerWatcher
from user_managment import ClientHandler,OsTools
from consol import Argument
import json
import os
from network_manager import NetworkManager
from doc_generator import DocGenerator
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
            self.stricker_connection_num = self.conf_dict["STRICKER_BANNING_CONNECTION_NUM"]


class XrayHandler:
    def __init__(self):
        self.system_conf = Config("/root/Xray-ClientManager/conf.json")
        self.client_handler = ClientHandler(self.system_conf.xray_conf)
        self.arguments = Argument()
        self.doc = DocGenerator()
        # Configuration For Stricker Watcher
        self.watcher = StrickerWatcher(check_period=0,
            access_dir= self.system_conf.access_dir,
            bannig_on= self.system_conf.banning_on,
            debug= self.system_conf.debug,
            banning_connection_exceed= self.system_conf.stricker_connection_num
            )
    
    def _get_user_vmess_all_conf(self,email,domain,vpn_name,cdn):
        print("----------------------------------------------------VMESS CDN URL-----------------------------------------------------------------\r\n")
        url_vmess_cdn_non_tls = self.client_handler.get_client_url_vmess_cdn_none_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vmess_cdn_non_tls,"CDN")
        print(url_vmess_cdn_non_tls)
        print("-------------------------------------------------VMESS DIRECT TLS URL-------------------------------------------------------------\r\n")
        url_vmess_direct_tls = self.client_handler.get_client_url_vmess_direct_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vmess_direct_tls,"TLS")
        print(url_vmess_direct_tls)
        print("--------------------------------------------------VMESS CDN TLS URL---------------------------------------------------------------\r\n")
        url_vmess_cdn_tls = self.client_handler.get_client_url_vmess_cdn_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vmess_cdn_tls,"TLS"+"-"+"CDN")
        print(url_vmess_cdn_tls)
        print("----------------------------------------------------------------------------------------------------------------------------------\r\n\r\n")

    def _get_user_vless_all_conf(self,email,domain,vpn_name,cdn):
        print("----------------------------------------------------VLESS XTLS-----------------------------------------------------------------\r\n")
        url_vless_xtls = self.client_handler.get_client_url_vless_tcp_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vless_xtls,"VLESS-TCP-XTLS")
        print(url_vless_xtls)
        print("-------------------------------------------------VLESS TCP URL-------------------------------------------------------------\r\n")
        url_vless_tcp_none_tls = self.client_handler.get_client_url_vless_tcp_none_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vless_tcp_none_tls,"VLESS-TCP")
        print(url_vless_tcp_none_tls)
        print("-------------------------------------------------VLESS WS TLS URL-------------------------------------------------------------\r\n")
        url_vless_WS_tls = self.client_handler.get_client_url_vless_ws_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vless_WS_tls,"VLESS-WS-TLS")
        print(url_vless_WS_tls)
        print("----------------------------------------------------------------------------------------------------------------------------------\r\n\r\n")

    def _get_config_v1(self,email,domain,vpn_name,cdn):
        print("----------------------------------------------------VMESS TCP OBFS-----------------------------------------------------------------\r\n")
        url_vmess_tcp_obfs = self.client_handler.get_client_url_vmess_tcp_obfussification(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vmess_tcp_obfs,"VMESS-TCP-OBFS")
        print(url_vmess_tcp_obfs)
        print("----------------------------------------------------VLESS XTLS-----------------------------------------------------------------\r\n")
        url_vless_xtls = self.client_handler.get_client_url_vless_tcp_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vless_xtls,"VLESS-TCP-TLS")
        print(url_vless_xtls)
        print("-------------------------------------------------VLESS WS TLS URL-------------------------------------------------------------\r\n")
        url_vless_WS_tls = self.client_handler.get_client_url_vless_ws_tls(email,domain,vpn_name,cdn)
        self.client_handler.get_client_qrcode(email,url_vless_WS_tls,"VLESS-WS-TLS")
        print(url_vless_WS_tls)
        print("----------------------------------------------------------------------------------------------------------------------------------\r\n\r\n")



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
                cdn: str = self.arguments.args.cdn
                vpn_name = vpn_name.replace(" ","+")
                profile = self.client_handler.get_client_profile(email)
                if not profile :
                    print("Error : No user Found")
                else : 
                    self._get_config_v1(email,domain,vpn_name,cdn)
                    


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
                email = self.arguments.args.email
                self.client_handler.del_user(email)
                # Here we Apply Changes if The Users specify it
                if self.arguments.args.apply :
                    self.client_handler.apply_changes()

            elif command == "get-all" :
                if self.arguments.args.domain == None :
                    print("error : Please Enter The Domain name with |-i domain-name|")
                    exit()
                if self.arguments.args.name == None :
                    print("error : Please Enter The vpn name  with |-n vpn-name|")
                    exit()

                domain:str =  self.arguments.args.domain
                vpn_name:str =  self.arguments.args.name
                cdn: str = self.arguments.args.cdn
                clients_email = self.client_handler.get_clients_email_list()
                clients_uuid_list = self.client_handler.get_clients_uuid_list()
                for index in range(len(clients_email)) :
                    print(f"\r\n\r\n--------------------------------------------------{clients_email[index]}-----------------------------------------------------------------\r\n")
                    self._get_config_v1(clients_email[index],domain,vpn_name,cdn)
                    
                for index in range(len(clients_email)) :   
                    self.doc.generate_docx(
                        email=clients_email[index],
                        uuid= clients_uuid_list[index]
                    )

                    

                

                

            




def main():   
    consol = XrayHandler()
    consol.consol_start()
    
    

if __name__ == "__main__":
    main()
