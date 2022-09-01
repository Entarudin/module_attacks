from models import Host, Network


class NetworkService:
    def __filter_out_hosts_with_ports(self, hosts: list[Host]) -> list[Host]:
        result = [
            host
            for host
            in hosts
            if host.ports
        ]

        return result

    def get_network_with_ports(self, network: Network) -> Network:
        network.tcp_hosts = self.__filter_out_hosts_with_ports(network.tcp_hosts)
        network.udp_hosts = self.__filter_out_hosts_with_ports(network.udp_hosts)
        return network
