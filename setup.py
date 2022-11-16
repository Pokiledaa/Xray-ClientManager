import os 
from statics import Directories




# Making program required Direcory 
os.mkdir(Directories.LOG_DIR)
#Creating The Sticker File
with open(Directories.STRICKER_DIR,"x") as s_f:
    pass

#Creating The Banned File
with open(Directories.BANNED_DIR,"x") as b_f:
    pass