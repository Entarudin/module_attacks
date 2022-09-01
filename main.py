from structure import (
    network_translator,
    network_service,
    json_service,
    attack_service,
    target_service
)


def main():
    data = json_service.parse_in_dict('data.json')
    network = network_translator.from_json(data)
    network_with_ports = network_service.get_network_with_ports(network)

    targets_tcp = target_service.cast_hosts_in_targets(network_with_ports.tcp_hosts)
    targets_udp = target_service.cast_hosts_in_targets(network_with_ports.udp_hosts)

    tcp_attacks = attack_service.create_attacks(targets_tcp, 'syn_flood')
    upd_attacks = attack_service.create_attacks(targets_udp, 'udp_flood')

    for item in upd_attacks:
        print(item.target.ip_address, item.target.status, item.target.port_id, item.status, item.contex)


if __name__ == '__main__':
    main()
