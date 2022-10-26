from scapy.arch import get_if_hwaddr
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, ICMP, UDP
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import sr1, srp, sendp
from scapy.utils import mac2str
import random

from models import ArpTableItem


class ScapyWrapper:
    def get_ip_gateway(self) -> str:
        packet = sr1(IP(dst="www.slashdot.org", ttl=0) / ICMP() / "XXXXXXXXXXX")
        return packet.src

    def arp_scan(self, ip) -> list[ArpTableItem]:
        request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
        answers_packets, unanswered_packets = srp(request, timeout=2, retry=1)
        result = []

        for sent, received in answers_packets:
            arp_table_item = ArpTableItem()
            arp_table_item.ip_address = received.psrc
            arp_table_item.mac_address = received.hwsrc
            result.append(arp_table_item)

        return result

    def send_dhcp_discover_packet(self, network_interface: str):
        discover_packet = self.__build_discover_packet(network_interface)
        sendp(discover_packet, iface=network_interface)

    def __build_discover_packet(self, network_interface):
        src_mac = get_if_hwaddr(network_interface)
        my_mac_address = '40:b8:9a:a1:e7:f5'  # might have to be changed for other networks
        spoofed_mac_address = my_mac_address
        options = [("message-type", "discover"),
                   ("max_dhcp_size", 1500),
                   ("client_id", mac2str(spoofed_mac_address)),
                   ("lease_time", 10000),
                   ("end", "0")]
        transaction_id = random.randint(1, 900000000)
        discover_packet = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff") \
                          / IP(src="0.0.0.0", dst="255.255.255.255") \
                          / UDP(sport=68, dport=67) \
                          / BOOTP(chaddr=[spoofed_mac_address],
                                  xid=transaction_id,
                                  flags=0xFFFFFF) \
                          / DHCP(options=options)
        return discover_packet
