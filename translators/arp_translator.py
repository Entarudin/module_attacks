from models import Arp


class ArpTranslator:
    def to_dict(self, model: Arp) -> dict:
        return {
            "ip_address": model.ip_address,
            "mac_address": model.mac_address,
        }