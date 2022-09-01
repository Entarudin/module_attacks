from typing import Literal


class ShellCommandTranslator:
    def to_shell_command_attack(
            self,
            ip_address: str,
            port_id: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood"],
    ) -> str:
        if type_attack == 'syn_flood':
            return self.__to_shell_syn_flood_attack(ip_address, port_id, count_packets=5)
        if type_attack == 'udp_flood':
            return self.__to_shell_udp_flood_attack(ip_address, port_id, count_packets=5)

    def __to_shell_syn_flood_attack(
            self,
            ip_address: str,
            port_id: str,
            count_packets: int
    ) -> str:
        attack_command =  \
            f"hping3 " \
            f"-S " \
            f"{ip_address}" \
            f" -p {port_id}" \
            f" -c {count_packets}"
        return attack_command

    def __to_shell_udp_flood_attack(
            self,
            ip_address: str,
            port_id: str,
            count_packets: int
    ) -> str:
        attack_command =  \
            f"hping3 " \
            f"--udp " \
            f"{ip_address}" \
            f" -p {port_id}" \
            f" -c {count_packets}"
        return attack_command
