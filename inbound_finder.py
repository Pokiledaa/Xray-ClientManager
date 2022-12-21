

class InboundSetting:
    def __init__(
            self,
            listen: str,
            port: int,
            protocol: str,
            network: str,
            path: str,
            security: str,
            alpn: list[str],
            flow: str,

        ):
        self.listen = listen
        self.port = port 
        self.protocol = protocol
        self.network = network
        self.path = path
        self.security = security
        self.alpn = alpn
        self.flow = flow

    
    @staticmethod
    def inbound_from_json(json_inbound: dict):
      
        listen = json_inbound.get("listen")
        port = json_inbound.get("port")
        protocol = json_inbound.get("protocol")
        try :
            network = json_inbound["streamSettings"]["network"]
        except KeyError:
            # Maybe Exiting Program for unsupported Config File
            network = "ws"
        try :
            path = json_inbound["streamSettings"]["wsSettings"]["path"]
        except KeyError:
            # Maybe Exiting Program for unsupported Config File
            path = ""
        try:
            security = json_inbound["streamSettings"]["security"]
        except KeyError :
            # Maybe Exiting Program for unsupported Config File
            security = "auto"

        try:
            alpn = json_inbound["streamSettings"]["xtlsSettings"]["alpn"]
        except KeyError :
            # Maybe Exiting Program for unsupported Config File
            alpn = [
                "h2",
                "http/1.1"
            ]
        try:
            flow = json_inbound["streamSettings"]["settings"]["clients"][0]
        except KeyError:
            # Maybe Exiting Program for unsupported Config File
            flow = "none"

        return InboundSetting(
            listen=listen,
            port=port,
            protocol=protocol,
            network=network,
            path=path,
            security=security,
            alpn=alpn,
            flow = flow
        )

            
        



