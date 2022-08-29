from attack_item import AttackItem
from pprint import pprint


class NmapReportTranslator:
    def __init__(
            self,
            report: dict,
    ):
        self.report = report

    def cast_tuple_in_str(self, value: tuple) -> str:
        return ''.join(value)

    def to_tcp(self, ):
        ip_address = ''
        port_id = ''
        state_port = ''
        service_port = ''
        protocol_port = ''
        result = []
        tcp_report_host = self.report['tcp_ports']['nmaprun']['host']
        for host in tcp_report_host:
            address = host['address']
            if isinstance(address, list):
                ip_address = host['address'][0]['@addr']
            if isinstance(address, dict):
                ip_address = host['address']['@addr']

            if 'port' in host['ports']:
                ports = host['ports']['port']
                for port in ports:
                    port_id = port['@portid'][0]
                    protocol_port = port['@protocol']
                    state_port = port['state']['@state'][0]
                    service_port = port['service']['@name'][0]
                    pprint(port_id)
                    result.append(
                        AttackItem(ip_address, port_id, state_port, service_port, protocol_port)
                    )
                    pprint(result)

        return result
