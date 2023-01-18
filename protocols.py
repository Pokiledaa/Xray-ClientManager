#!/usr/bin/env python3

from abc import ABC,abstractmethod
from enum import Enum
from inbound_finder import InboundSetting
import os


class EnviromentVariables(str,Enum):
    VPN_NAME = "VPN_NAME"
    DOMAIN_NAME = "DOMAIN_NAME"
    CND_NAME = "CDN_NAME"


class V2rayConfig:
    def __init__(self) -> None:
        pass



class Protocols:
    def __init__(self) -> None:
        self.vpn_name = self.get_vpn_name()
        self.domain_name = self.get_domain_name()
        self.cdn_name = self.get_cdn_name()

    def get_vpn_name(self,name= ""):
        if(name == ""):
            name = os.getenv(EnviromentVariables.VPN_NAME,"ERROR")
        return name

    def get_domain_name(self,domain= ""):
        if domain == "":
            domain  = os.getenv(EnviromentVariables.DOMAIN_NAME,"ERROR")
        return domain

    def get_cdn_name(self,cdn= ""):
        if cdn == "":
            cdn = os.getenv(EnviromentVariables.CND_NAME,"ERROR")
        return cdn




class Vmess(Protocols):
    def __init__(self) -> None:
        super().__init__()
        self.vmess_dict_base = {
            "v": "2",
            "ps": "",
            "add": "",
            "port": "",
            "id": "",
            "aid": "",
            "scy": "",
            "net": "",
            "type": "",
            "host": "",
            "path": "",
            "tls": "",
            "sni": "",
            "alpn": ""
        }

 

    def _base(self):
        # setting the vpn name
        self.vmess_dict_base["ps"] = self.domain_name

    def url_ws_tls_nginx(self,id, inboubd: InboundSetting,append_vpn_name: str):
        vmess_dict = self.vmess_dict_base
        vmess_dict["ps"] = (self.vpn_name + append_vpn_name)
        vmess_dict["add"] = self.domain_name
        vmess_dict["port"] = 443
        vmess_dict["id"] = id
        vmess_dict["aid"] = 0
        vmess_dict["scy"] = "chacha20-poly1305"
        vmess_dict["net"] = inboubd.network
        vmess_dict["type"] = "none"
        vmess_dict["host"] = ""
        vmess_dict["path"] = inboubd.path
        vmess_dict["tls"] = "tls"
        vmess_dict["sni"] = self.domain_name
        vmess_dict["alpn"] = ""

        return vmess_dict

    def url_ws_tls_nginx_proxy(self,id, inboubd: InboundSetting,append_vpn_name: str):
        vmess_dict = self.vmess_dict_base
        vmess_dict["ps"] = (self.vpn_name + append_vpn_name)
        vmess_dict["add"] = self.cdn_name
        vmess_dict["port"] = 443
        vmess_dict["id"] = id
        vmess_dict["aid"] = 0
        vmess_dict["scy"] = "chacha20-poly1305"
        vmess_dict["net"] = inboubd.network
        vmess_dict["type"] = "none"
        vmess_dict["host"] = ""
        vmess_dict["path"] = inboubd.path
        vmess_dict["tls"] = "tls"
        vmess_dict["sni"] = self.domain_name
        vmess_dict["alpn"] = ""

        return vmess_dict


    def url_ws_tls(self,id, inboubd: InboundSetting,append_vpn_name: str):
        vmess_dict = self.vmess_dict_base
        vmess_dict["ps"] = (self.vpn_name + append_vpn_name)
        vmess_dict["add"] = self.domain_name
        vmess_dict["port"] = inboubd.port
        vmess_dict["id"] = id
        vmess_dict["aid"] = 0
        vmess_dict["scy"] = "chacha20-poly1305"
        vmess_dict["net"] = inboubd.network
        vmess_dict["type"] = "none"
        vmess_dict["host"] = ""
        vmess_dict["path"] = inboubd.path
        vmess_dict["tls"] = "tls"
        vmess_dict["sni"] = self.domain_name
        vmess_dict["alpn"] = inboubd.alpn

        return vmess_dict

    def url_tcp_obfs(self,id, inboubd: InboundSetting,append_vpn_name: str):
        
        vmess_dict = self.vmess_dict_base
        vmess_dict["ps"] = (self.vpn_name + append_vpn_name)
        vmess_dict["add"] = self.cdn_name
        vmess_dict["port"] = inboubd.port
        vmess_dict["id"] = id
        vmess_dict["aid"] = 0
        vmess_dict["scy"] = "chacha20-poly1305"
        vmess_dict["net"] = inboubd.network
        vmess_dict["type"] = inboubd.tcp_setting_header_type
        vmess_dict["host"] = "www.google.com"
        vmess_dict["path"] = inboubd.path
        vmess_dict["tls"] = ""
        vmess_dict["sni"] = ""
        vmess_dict["alpn"] = ""

        return vmess_dict



        




