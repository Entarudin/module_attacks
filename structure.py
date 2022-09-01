from translators import (
    PortTranslator,
    HostTranslator,
    NetworkTranslator,
    ShellCommandTranslator,
    ListTranslator,
)

from services import (
    InvokerShellCommandService,
    NetworkService,
    JsonService,
    AttackService,
    TargetService,
    ResultAttackService
)

port_translator = PortTranslator()
ports_translator = ListTranslator(port_translator)

host_translator = HostTranslator(ports_translator)
hosts_translator = ListTranslator(host_translator)

network_translator = NetworkTranslator(hosts_translator)
network_service = NetworkService()

shell_command_translator = ShellCommandTranslator()
invoker_shell_command_service = InvokerShellCommandService()

json_service = JsonService()
target_service = TargetService()
result_attack_service = ResultAttackService()

attack_service = AttackService(
    shell_command_translator,
    invoker_shell_command_service,
    target_service,
    result_attack_service
)
