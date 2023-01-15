from structure import (
    network_translator,
    network_service,
    attack_service,
    target_service,
    scapy_wrapper,
    network_json_repository,
    attacks_translator,
)

UDP_FLOOD = 'udp_flood'
SYN_FLOOD = 'syn_flood'
ARP_SPOOFING = 'arp_spoofing'
BRUTE_FORCE = 'brute_force'
DHCP_STARVATION = 'dhcp_starvation'
DHCP_SPOOFING = 'dhcp_spoofing'


def start_attacks():
    network_data = network_json_repository.parse_in_dict('data.json')
    network = network_translator.from_json(network_data)
    network_with_ports = network_service.filter_out_network_with_ports(network)
    current_ip_address_with_subnet = f"{network.current_ip_address}/24"
    targets_tcp = target_service.cast_hosts_in_targets(network_with_ports.tcp_hosts)
    targets_udp = target_service.cast_hosts_in_targets(network_with_ports.udp_hosts)
    merged_network_with_ports_hosts = network_with_ports.tcp_hosts + \
                                      network_with_ports.udp_hosts + network_with_ports.ip_hosts

    targets_brute_force = target_service.cast_hosts_in_targets_brute_force(merged_network_with_ports_hosts)
    brute_force_attacks = attack_service.create_attacks(targets_brute_force, BRUTE_FORCE)
    syn_flood_attacks = attack_service.create_attacks(targets_tcp, SYN_FLOOD)
    udp_flood_attacks = attack_service.create_attacks(targets_udp, UDP_FLOOD)
    ip_gateway = scapy_wrapper.get_ip_gateway()
    arp_table = scapy_wrapper.arp_scan(current_ip_address_with_subnet)
    arp_targets = target_service.cast_arp_table_in_targets(arp_table)
    arp_flood_attacks = attack_service.create_attacks(arp_targets, ARP_SPOOFING, ip_gateway)
    dhcp_stavation_attacks = attack_service.create_dhcp_starvation_attack(network.current_networks_interface)
    dhcp_spoofing_attacks = attack_service.create_dhcp_spoofing_attack(network.current_networks_interface,
                                                                       network.current_ip_address)
    return {
        "syn_flood_attacks": attacks_translator.to_dict(syn_flood_attacks),
        "udp_flood_attacks": attacks_translator.to_dict(udp_flood_attacks),
        "arp_flood_attacks": attacks_translator.to_dict(arp_flood_attacks),
        "brute_force_attacks": attacks_translator.to_dict(brute_force_attacks),
        "dhcp_stavation_attack": attacks_translator.to_dict(dhcp_stavation_attacks),
        "dhcp_spoofing_attack": attacks_translator.to_dict(dhcp_spoofing_attacks)
    }
