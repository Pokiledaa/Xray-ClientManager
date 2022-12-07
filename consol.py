from argparse import ArgumentParser

class Argument :
    def __init__(self) :
        self.parser= ArgumentParser(description="<<Welcome TO the Xray-tools>>")
        self.sub_parser = self.parser.add_subparsers(dest="command")

        self.get_user_parser = self.sub_parser.add_parser("get",help="Returning The User From Config File ")
        self.get_user_parser.add_argument("email",type=str)
        self.get_user_parser.add_argument("-d","--domain",type=str)
        self.get_user_parser.add_argument("-c","--cdn",type=str)
        self.get_user_parser.add_argument("-n","--name",type=str)

        self.add_user_parser = self.sub_parser.add_parser("add",help="Adding The user to The Config File ")
        self.add_user_parser.add_argument("raw",type=str)
        self.add_user_parser.add_argument("-a","--apply",action="store_true")

        # Check For Stricker Menu
        self.stricker_check_parser = self.sub_parser.add_parser("check",help="Checking For Stricker")
        self.stricker_check_parser.add_argument("-w","--wait",type=int)
        # Apply changes on Xray Menu
        self.apply_parser = self.sub_parser.add_parser("apply",help="Applying Changes On the Xray Config File")
        # Unvalidate The Client Menu
        self.unvalidator_parser = self.sub_parser.add_parser("unvalidate",help="Unvalidate The Client")
        self.unvalidator_parser.add_argument("email",type=str)
        # validate The banned Client Menu
        self.validator_parser = self.sub_parser.add_parser("validate",help="validat The Banned Client")
        self.validator_parser.add_argument("email",type=str)
        # Delet Client Menu
        self.del_parser = self.sub_parser.add_parser("del",help="Delete The Client")
        self.del_parser.add_argument("email",type=str)
        # Get All Clients Menu
        self.get_all_users_parser = self.sub_parser.add_parser("get-all",help="Returning All Users From Config File")
        self.get_all_users_parser.add_argument("-d","--domain",type=str)
        self.get_all_users_parser.add_argument("-c","--cdn",type=str)
        self.get_all_users_parser.add_argument("-n","--name",type=str)
       
        




    def start(self):
        # here We Parse Our Args             
        self.args =  self.parser.parse_args()
