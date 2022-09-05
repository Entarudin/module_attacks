from typing import Literal, Optional


class ShellCommandTranslator:
    def to_shell_command_attack(
            self,
            ip_address: str,
            port_id: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood"],
    ) -> Optional[str]:
        type_to_func_mapping = {
            "syn_flood": self.__to_shell_syn_flood_attack,
            "udp_flood": self.__to_shell_udp_flood_attack,
        }
        return type_to_func_mapping[type_attack](ip_address, port_id, count_packets=5)

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
