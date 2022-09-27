from scapy.all import (sr1, IP, ICMP, Ether, ARP, srp)
from models import Arp


class ScapyService:
    def get_ip_gateway(self) -> str:
        p = sr1(
            IP(dst="www.slashdot.org", ttl=0) / ICMP() / "XXXXXXXXXXX"
        )
        return p.src

    def arp_scan(self, ip) -> list[ARP]:
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)

        ans, unans = srp(request, timeout=2, retry=1)
        result = []

        for sent, received in ans:
            arp = Arp()
            arp.ip_address = received.psrc
            arp.mac_address = received.hwsrc
            result.append(arp)

        return result