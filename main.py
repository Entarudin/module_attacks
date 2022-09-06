from structure import (
    network_translator,
    network_service,
    json_service,
    attack_service,
    target_service
)

UDP_FLOOD = 'udp_flood'
SYN_FLOOD = 'syn_flood'


def main():
    data = json_service.parse_in_dict('data.json')
    network = network_translator.from_json(data)
    network_with_ports = network_service.get_network_with_ports(network)

    targets_tcp = target_service.cast_hosts_in_targets(network_with_ports.tcp_hosts)
    targets_udp = target_service.cast_hosts_in_targets(network_with_ports.udp_hosts)

    tcp_attacks = attack_service.create_attacks(targets_tcp, SYN_FLOOD)
    upd_attacks = attack_service.create_attacks(targets_udp, UDP_FLOOD)

    json_service.write_in_file('result.json', tcp_attacks, upd_attacks)


if __name__ == '__main__':
    main()
