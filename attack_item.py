class AttackItem:
    def __init__(
            self,
            ip_address: str,
            port_id: str,
            state_port: str,
            service_port: str,
            protocol_port: str,
    ):
        self.ip_address = ip_address,
        self.port_id = port_id,
        self.state_port = state_port,
        self.service_port = service_port,
        self.protocol_port = protocol_port

    def __repr__(self):
        return f"{self.__class__}\n" \
               f"{self.ip_address = }\n" \
               f"{self.port_id = }\n" \
               f"{self.state_port = }\n" \
               f"{self.service_port = }\n" \
               f"{self.protocol_port }\n"
