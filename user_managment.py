import qrcode
import json
import subprocess
import base64

class ClientHandler :
    def __init__(
        self,
        xray_conf_dir,
    ):
        self.xray_conf_dir = xray_conf_dir


       

    def _read_json_conf(self):
        js = None
        with open(self.xray_conf_dir,"r") as xray_config :
            js = json.load(xray_config)

        xray_config.close()

        return js

    def _read_inbounds(self,js_conf)-> dict :
        # TODO : Here We should choose beatwean Inbounds and check them
        inbounds:dict = js_conf["inbounds"][0]
        return inbounds

    def read_clients(self,inbound)-> list:
        clients: list = inbound["settings"]["clients"]
        return clients

    def read_client_emails(self,clients: list)-> list:
        client_list: list = []
        for client in clients :
            client_list.append(client["email"])
   
        return client_list

    def get_client_profile(self,email: str):
        js = self._read_json_conf()
        inbound = self._read_inbounds(js)
        clients = self.read_clients(inbound)

        profile: dict = {}

        for client in clients :
            if client["email"] == email :
                profile = client
                break

        return profile

    def get_client_url(self, email: str, domain: str, vpn_name: str):
        profile = self.get_client_profile(email)

        url: str = "vless://"+profile["id"]+"@"+domain+"?path=%2Fuser"+"&"+"security=none"+"&"+"encryption=none"+"&"+"type=ws"+"#"+vpn_name

        return url

    def get_client_qrcode(self,email: str, url: str):
        profile = self.get_client_profile(email)
        image = qrcode.make(url)
        image_name = profile["email"].split("-")
        if len(image_name) == 1:
            image.save(image_name[0]+".PNG")
        elif len(image_name) == 5:
            image.save(image_name[1]+"-"+image_name[2]+".PNG")


    def generate_uuid(self)-> str:
        temp = subprocess.check_output(['xray.exe', 'uuid'])
        uuid = temp.decode("utf-8").strip()
        return uuid

    def add_profile(self,max_conn: int,ph_numer: int,name: str,start_time: str,duration: int):
        '''
            Important Should Check if The User Already Exist or No 
            Step That Should Be done Here : 
            1 - Making The Email String FORMAT : | max_conn@phone_number-first_name-last_name-start_time_duration |
            2 - Genrating The UUID Using The xray command line 
            3 - making the desired Profile 
            4 - reading the config file 
            5 - appending the profile on it
            6 - recreating the json file 
            7 - closing the file
            8 - systemctl restart the xray service
            9 - getting the status 
            10 - if the problem found redoing the thing and puting the prevoius config file
        '''
        # 1
        max_conn = str(max_conn)
        ph_numer = str(ph_numer)
        duration = str(duration)
        full_name = name.split(" ")
        first_name = ""
        last_name = ""
        # 2 
        id = self.generate_uuid()
        if len(full_name) == 1:
            first_name = full_name[0]
            last_name = full_name[1]            
        elif len(full_name) == 2 :
            first_name = full_name[0]
            last_name = full_name[1]
        # 3
        email:str = max_conn+"@"+ph_numer+"-"+first_name+"-"+last_name+"-"+start_time+"-"+duration
        # Here we check if The User ALready Exist or Not
        exsistance = self.get_client_profile(email)
        if exsistance :
            return 0

        profile = {
            "id": id,
            "email": email,
            "level": 1
        }
        # 4 
        js = self._read_json_conf()
        # 5
        js["inbounds"][0]["settings"]["clients"].append(profile)
        # 6
        with open(self.xray_conf_dir,"w") as xray_config :
            json.dump(js,xray_config,indent=4)
        # 7
        xray_config.close()
        return 1

    def add_user(self,max_conn: int,ph_numer: int,name: str,start_time: str,duration: int):
        result = self.add_profile(max_conn, ph_numer ,name ,start_time ,duration)
        if result :
            print("INFO : User Added !!")
        else :
            print("User Already Exsist(Override)")


        




class OsTools:
    def __init__(self):
        self.command = "xray"






# class ClientManager:
#     def __init__(
#         self,
#         xray_conf_dir,
#     ):

#         self.xray_conf_dir = xray_conf_dir
#         self.xray_conf_file = None
#         self.xray_conf = None
#         self.clients_json: dict = {}
#         self.client_profile: dict = {}
#         self.client_profiles: list = []

#         self._read_conf()



#     def _read_conf(self):
#         self.xray_conf_file = open(self.xray_conf_dir,"r")
#         self.xray_conf = self.xray_conf_file.read()
#         self.xray_conf_file.close()

#     def _read_clients(self):
#         self.clients_json = json.loads(self.xray_conf)
#         inbounds = self.clients_json["inbounds"][0]
#         settings = inbounds["settings"]
#         self.client_profiles = settings["clients"]

#         return self.client_profiles
  
       
#     def get_client(self, email: str):
#         # Maybe Parsing The name Only???
#         self._read_clients()    
#         target_client: dict = {}
#         for client in self.client_profiles :
#             if client["email"] == email :
#                 target_client = client
#                 break

#         return target_client

#     def get_client_email(self):

#         client_list: list = []

#         self._read_clients()    
#         for client in self.client_profiles:
#            client_list.append(client["email"])

#         return client_list



        

#     def generat_client_url(self, client ,domain: str , vpn_name: str) -> str:

#         client:dict = self.get_client(client)

#         client_uuid = client["id"]
#         client_email = client["email"]

#         client_full_json: dict = {
#             "v": "2",
#             "ps": vpn_name,
#             "add": domain,
#             "port": "80",
#             "id": client_uuid,
#             "aid": "0",
#             "scy": "auto",
#             "net": "ws",
#             "type": "none",
#             "host": "",
#             "path": "/user",
#             "tls": "",
#             "sni": "",
#             "alpn": ""
#         }
#         # Making Base 64 Clients
#         dumped = json.dumps(client_full_json)
#         message_bytes = dumped.encode('ascii')
#         base64_bytes = base64.b64encode(message_bytes)
#         base64_message = base64_bytes.decode('ascii')
#         final_profile = "vmess://"+ base64_message
#         return final_profile,client_email


#     def generate_qr(self, url, client):
#         image = qrcode.make(url)
#         image.save(client+".PNG")

#     def get_clinet_property(self, email) ->dict:
#         prop: dict = self.get_client(email)
#         if len(prop) :

#             full_profile: dict = {}

#             user_uuid = str(prop['id'])
#             #user_email = str(prop['email'])
#             user_email = "2@091245585-parsa-oskouie-1401/5/8-1401/7/8"
#             parsed_email= user_email.split("@")
#             max_connection = parsed_email[0]
#             client_prop_unparsed = parsed_email[1]

#             client_prop_parsed: list = client_prop_unparsed.split("-") 
#             print(len(client_prop_parsed))

#             if len(client_prop_parsed) == 5:
#                 full_profile ={
#                     'Id': user_uuid,
#                     'Num/TId': client_prop_parsed[0],
#                     'Name': client_prop_parsed[1],
#                     'LastName': client_prop_parsed[2],
#                     'Start_Time': client_prop_parsed[3],
#                     'End_Time':client_prop_parsed[4]
#                 }
#             else :
#                 full_profile ={
#                     'Id': user_uuid,
#                     'Num/TId': client_prop_unparsed,
#                     'Name': 'Unknown' ,
#                     'LastName': 'Unknown',
#                     'Start_Time': 'Unknown',
#                     'End_Time': 'Unknown'
#                 }

#             return full_profile            
#         else:
#             print(prop)
#             print("User Not Found")

#     def generate_uuid(self)-> str:
#         temp = subprocess.check_output(['xray', 'uuid'])
#         uuid = temp.decode("utf-8").strip()
#         return uuid


#     def add_user(self, user_identity: str):
#         #self._read_conf()
#         profiles = self._read_clients()
#         #print(self.client_profiles)
#         user_uuid = self.generate_uuid()
#         user_dict = {
#             'id': user_uuid,
#             'email': user_identity,
#             'level': 1,
#             'alterId': 0,
#         }

#         conf = json.loads(self.xray_conf)
#         conf["inbounds"][0]["settings"]["clients"].append(user_dict)
#         json_conf =  json.dumps(conf, 
#                         indent=4,  
#                         separators=(',',': '))
#         print(json_conf)