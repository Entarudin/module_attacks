from typing import Optional


class Arp:
    def __init__(self):
        self.ip_address: Optional[str] = None
        self.mac_address: Optional[str] = None
