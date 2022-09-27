from structure import (
    network_translator,
    network_service,
    json_service,
    attack_service,
    target_service,
    scapy_service,
)

UDP_FLOOD = 'udp_flood'
SYN_FLOOD = 'syn_flood'
ARP_SPOOFING = 'arp_spoofing'


def main():
    data = json_service.parse_in_dict('data.json')
    network = network_translator.from_json(data)
    network_with_ports = network_service.get_network_with_ports(network)
    current_ip_address = f"{network.current_ip_address}/24"
    targets_tcp = target_service.cast_hosts_in_targets(network_with_ports.tcp_hosts)
    targets_udp = target_service.cast_hosts_in_targets(network_with_ports.udp_hosts)
    tcp_attacks = attack_service.create_attacks(targets_tcp, SYN_FLOOD)
    upd_attacks = attack_service.create_attacks(targets_udp, UDP_FLOOD)

    ip_gateway = scapy_service.get_ip_gateway()
    arp_table = scapy_service.arp_scan(current_ip_address)
    arp_targets = target_service.cast_arp_table_in_targets(arp_table)
    arp_attacks = attack_service.create_attacks(arp_targets, ARP_SPOOFING, ip_gateway)
    json_service.write_in_file('result.json', tcp_attacks, upd_attacks, arp_attacks)


if __name__ == '__main__':
    main()
