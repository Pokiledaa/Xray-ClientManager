#!/usr/bin/env python3

import json
import base64
import qrcode
import subprocess

from stricker_watcher import StrickerWatcher





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



class ClientManager:
    def __init__(
        self,
        xray_conf_dir,
    ):

        self.xray_conf_dir = xray_conf_dir
        self.xray_conf_file = None
        self.xray_conf = None
        self.clients_json: dict = {}
        self.client_profile: dict = {}
        self.client_profiles: list = []

        self._read_conf()



    def _read_conf(self):
        self.xray_conf_file = open(self.xray_conf_dir,"r")
        self.xray_conf = self.xray_conf_file.read()
        self.xray_conf_file.close()

    def _read_clients(self):
        self.clients_json = json.loads(self.xray_conf)
        inbounds = self.clients_json["inbounds"][0]
        settings = inbounds["settings"]
        self.client_profiles = settings["clients"]

        return self.client_profiles
  
       
    def get_client(self, email: str):
        # Maybe Parsing The name Only???
        self._read_clients()    
        target_client: dict = {}
        for client in self.client_profiles :
            if client["email"] == email :
                target_client = client
                break

        return target_client

    def get_client_email(self):

        client_list: list = []

        self._read_clients()    
        for client in self.client_profiles:
           client_list.append(client["email"])

        return client_list



        

    def generat_client_url(self, client ,domain: str , vpn_name: str) -> str:

        client:dict = self.get_client(client)

        client_uuid = client["id"]
        client_email = client["email"]

        client_full_json: dict = {
            "v": "2",
            "ps": vpn_name,
            "add": domain,
            "port": "80",
            "id": client_uuid,
            "aid": "0",
            "scy": "auto",
            "net": "ws",
            "type": "none",
            "host": "",
            "path": "/user",
            "tls": "",
            "sni": "",
            "alpn": ""
        }
        # Making Base 64 Clients
        dumped = json.dumps(client_full_json)
        message_bytes = dumped.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        final_profile = "vmess://"+ base64_message
        return final_profile,client_email


    def generate_qr(self, url, client):
        image = qrcode.make(url)
        image.save(client+".PNG")

    def get_clinet_property(self, email) ->dict:
        prop: dict = self.get_client(email)
        if len(prop) :

            full_profile: dict = {}

            user_uuid = str(prop['id'])
            #user_email = str(prop['email'])
            user_email = "2@091245585-parsa-oskouie-1401/5/8-1401/7/8"
            parsed_email= user_email.split("@")
            max_connection = parsed_email[0]
            client_prop_unparsed = parsed_email[1]

            client_prop_parsed: list = client_prop_unparsed.split("-") 
            print(len(client_prop_parsed))

            if len(client_prop_parsed) == 5:
                full_profile ={
                    'Id': user_uuid,
                    'Num/TId': client_prop_parsed[0],
                    'Name': client_prop_parsed[1],
                    'LastName': client_prop_parsed[2],
                    'Start_Time': client_prop_parsed[3],
                    'End_Time':client_prop_parsed[4]
                }
            else :
                full_profile ={
                    'Id': user_uuid,
                    'Num/TId': client_prop_unparsed,
                    'Name': 'Unknown' ,
                    'LastName': 'Unknown',
                    'Start_Time': 'Unknown',
                    'End_Time': 'Unknown'
                }

            return full_profile            
        else:
            print(prop)
            print("User Not Found")

    def generate_uuid(self)-> str:
        temp = subprocess.check_output(['xray', 'uuid'])
        uuid = temp.decode("utf-8").strip()
        return uuid


    def add_user(self, user_identity: str):
        #self._read_conf()
        profiles = self._read_clients()
        #print(self.client_profiles)
        user_uuid = self.generate_uuid()
        user_dict = {
            'id': user_uuid,
            'email': user_identity,
            'level': 1,
            'alterId': 0,
        }

        conf = json.loads(self.xray_conf)
        conf["inbounds"][0]["settings"]["clients"].append(user_dict)
        json_conf =  json.dumps(conf, 
                        indent=4,  
                        separators=(',',': '))
        print(json_conf)
        
        

        
        # user_json =json.dumps(user_dict)
        
        # parsed_input: list = user_identity.split("@")
        # connestion_number = parsed_input[0]
        # identity = parsed_input[1]
        # user_prop:list = identity.split("-")
        # print(user_prop)
        
        # print(connestion_number)
        # print(identity)

        
        # user_uuid = None
        # user_email = None
        # user_model: dict = {
        #     'id': user_uuid,
        #     'email': user_identity,
        #     'level': 1,
        #     'alterId': 0
        # }







def main():
    system_conf = Config("conf.json")

    

    client_manager = ClientManager(system_conf.xray_conf)


    client_emials = client_manager.get_client_email()

#    print(client_manager.get_client("1@salehzadeh_aida"))

#    client_manager.add_user("2")

#   client_manager.add_user("2@091245585-parsa-oskouie-1401/5/8-1401/7/8")
   

#    client_manager.get_clinet_property("2@mohammad")

   #url,email = client_manager.generat_client_url("2@mohammad","weareiran.space","solh")

   #client_manager.generate_qr(url,email)


    watcher = StrickerWatcher(10)

    watcher.count_ip_per_user(client_emials)


   


if __name__ == "__main__":
    main()