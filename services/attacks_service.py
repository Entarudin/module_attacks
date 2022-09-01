from typing import Literal, Optional

from models import Attack, Target


class AttackService:
    def __init__(
            self,
            shell_command_translator,
            invoker_shell_command_service,
            target_service,
            result_attack_service
    ):
        self.shell_command_translator = shell_command_translator
        self.invoker_shell_command_service = invoker_shell_command_service
        self.target_service = target_service
        self.result_attack_service = result_attack_service

    def create_attack(
            self,
            ip_address: str,
            port_id: str,
            status_port: str,
            service: str,
            protocol: str,
            type_attack: Literal["syn_flood", "udp_flood"],
    ) -> Attack:

        attack = Attack()
        target = self.target_service.create_target(ip_address, port_id, status_port, service, protocol)
        contex = self.shell_command_translator.to_shell_command_attack(ip_address, port_id, protocol, type_attack)
        result = self.invoker_shell_command_service.execute_one_command(contex)
        status_attack = self.result_attack_service.check_status_attack(type_attack, result)
        attack.target = target
        attack.contex = contex
        attack.result = result
        attack.status = status_attack
        return attack

    def create_attacks(
            self,
            targets: list[Target],
            type_attack: Literal["syn_flood", "udp_flood"]
    ) -> list[Attack]:
        result = []
        for item in targets:
            attack = self.create_attack(
                item.ip_address,
                item.port_id,
                item.status,
                item.service,
                item.protocol,
                type_attack
            )
            result.append(attack)
        return result
