class ShellCommandsTranslator:
    def __init__(
            self,
            port: int,
            ip: str,
            flood_flag: str,
            count_packets: int
    ):
        self.port = port
        self.ip = ip
        self.flood_flag = flood_flag
        self.count_packets = count_packets

    def to_shell_command(self, ) -> str:
        shell_command = \
            f"hping3 " \
            f"{self.flood_flag} " \
            f"{self.ip}" \
            f" -p {self.port}" \
            f" -c {self.count_packets}"

        return shell_command
