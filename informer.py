# Not implemented Yet
import requests
import threading
from time import sleep

TOKEN = "YOUT TOKEN"
CHAT_ID = "YOUR CHAT ID"

class Informer:
    def __init__(self) -> None:
        self.token = TOKEN
        self.chat_id = "294598365"
        self.message = "None"

    def post_thread(self):
        url = url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={self.message}"
        requests.post(url)

    def inform_admin(self,message: str) :
        thread = threading.Thread(target=self.post_thread,daemon=True)
        self.message = message
        thread.start()




