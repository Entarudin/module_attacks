from scapy.all import *
from scapy.layers.dhcp import DHCP


class DhcpSniffer:
    def __init__(self, network_interface):
        self.network_interface = network_interface
        self.offer_count = 0
        self.status_attacks = []

    def start_dhcp_shiffer(self, condition_container):
        sniff(count=5,
              iface=self.network_interface,
              filter="udp and (port 67 or 68)",
              prn=self.__packet_handler,
              store=1)
        condition_container["condition_sniffer"] = self.__get_status_dhcp_spoofing()

    # Возвращает True в случае обнаружении атаки
    # False в случае неуспешной атаки
    def __get_status_dhcp_spoofing(self):
        count_successful_attacks = self.status_attacks.count(True)
        count_unsuccessful_attacks = self.status_attacks.count(False)
        return count_successful_attacks > count_unsuccessful_attacks

    def __packet_handler(self, packet):
        if DHCP in packet and packet[DHCP].options[0][1] == 2:
            self.offer_count = self.offer_count + 1
            print("Offer packet #" + str(self.offer_count))
            print(packet.summary())
            if self.offer_count > 1:
                print("XXXX" + str(self.offer_count) +
                      " DHCP Servers found in the network. Attacks might happen." + "XXXX")
                self.status_attacks.append(True)
