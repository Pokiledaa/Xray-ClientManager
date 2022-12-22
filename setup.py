import os 
from statics import Directories






# Making program required Direcory 
try:
    os.mkdir(Directories.LOG_DIR)
    print(f"{Directories.LOG_DIR} Created!!")
except FileExistsError :
    print(f"{Directories.LOG_DIR} Already Exsist")

#Creating The Sticker File
try :
    with open(Directories.STRICKER_DIR,"x") as s_f:
        print(f"{Directories.STRICKER_DIR} Created!!")
except FileExistsError :
    print(f"{Directories.STRICKER_DIR} Already Exsist")

#Creating The Banned File
try :
    with open(Directories.BANNED_DIR,"x") as b_f:
        print(f"{Directories.BANNED_DIR} Created!!")
except FileExistsError:
    print(f"{Directories.BANNED_DIR} Already Exsist")

#Creating The unvalidated File
try:
    with open(Directories.UNVALIDATED,"x") as u_f:
        print(f"{Directories.UNVALIDATED} Created!!")
except FileExistsError :
    print(f"{Directories.UNVALIDATED} Already Exsist")

#Creating The generated  QR Code output  folder
try:
    os.mkdir(Directories.GENERATED_OUTPUT)
    print(f"{Directories.GENERATED_OUTPUT} Created!!")
except FileExistsError :
    print(f"{Directories.GENERATED_OUTPUT} Already Exsist")

#Creating The generated DOCX output  folder
try:
    os.mkdir(Directories.GENERATED_DOCX)
    print(f"{Directories.GENERATED_DOCX} Created!!")
except FileExistsError :
    print(f"{Directories.GENERATED_DOCX} Already Exsist")


#Creating The Client Monitoring  File
try :
    os.mkdir(Directories.CLIENT_MONITORING_DIR)
    print(f"{Directories.CLIENT_MONITORING_DIR} Created!!")
except FileExistsError :
    print(f"{Directories.CLIENT_MONITORING_DIR} Already Exsist")



