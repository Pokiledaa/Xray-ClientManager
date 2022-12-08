from enum import Enum,IntEnum

UNVALID_UUID = "7b83fd6d-b2af-4731-8baa-31ef68617368"



class Directories(str,Enum):
    LOG_DIR = "log"
    BANNED_DIR = f"{LOG_DIR}/banned",
    STRICKER_DIR = f"{LOG_DIR}/strickers"
    UNVALIDATED = f"{LOG_DIR}/unvalidated"
    GENERATED_OUTPUT = "generated_qr_code"
    GENERATED_DOCX = "generated_docx"

class AddProfileResponseCode(IntEnum):
    NO_INBOUND_SELECTED = 1
    CLIENT_ALREADY_EXSIST = 2


class InboudType(str,Enum):
    VLESS = "vless"
    VMESS = "vmess"



class NetworkType(str,Enum):
    WS = "ws"