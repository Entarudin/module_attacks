from scapy.arch import get_if_hwaddr
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
from scapy.utils import mac2str
import random


class DhcpSendsPackets:
    def __init__(self, network_interface: str):
        self.network_interface = network_interface

    def send_dhcp_discover_packet(self):
        discover_packet = self.build_discover_packet()
        for item in range(0,10):
            import time
            time.sleep(1)
            sendp(discover_packet, iface=self.network_interface)

    def build_discover_packet(self):
        src_mac = get_if_hwaddr(self.network_interface)
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
