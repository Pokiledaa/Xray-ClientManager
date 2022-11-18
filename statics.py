from enum import Enum

UNVALID_UUID = "7b83fd6d-b2af-4731-8baa-31ef68617368"



class Directories(str,Enum):
    LOG_DIR = "log"
    BANNED_DIR = f"{LOG_DIR}/banned",
    STRICKER_DIR = f"{LOG_DIR}/strickers"
    UNVALIDATED = f"{LOG_DIR}/unvalidated"