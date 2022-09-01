from typing import Literal
from models import Network


class NetworkTranslator:
    def __init__(self, hosts_translator):
        self.hosts_translator = hosts_translator

    def from_json(self, json: dict) -> Network:
        network = Network()
        network.tcp_hosts = self.__get_hosts(json, "tcp")
        network.udp_hosts = self.__get_hosts(json, "udp")
        return network

    def __get_hosts(self, json, key: Literal["tcp", "udp"]):
        hosts_json = json.get(f"{key}_ports", {})\
            .get("nmaprun", {})\
            .get("host", [])
        return self.hosts_translator.from_json(hosts_json)


