from pprint import pprint

from shell_commands_executor import ShellCommandsExecutor
from shell_commands_translator import ShellCommandsTranslator
from nmap_reports_translator import NmapReportTranslator
import json

port = 80
ip = '192.168.0.1'
syn_flood_flag = '-S'
count_packets = 10


def check_success_syn_flood_attack(report: str) -> bool:
    list_report = report.split('\n')[1:]
    flag = ''
    for data in list_report:
        for item in data.split(' '):
            if 'flags' in item:
                chunks = item.split('=')
                flag = chunks[1]

    result = True if flag == 'SA' else False
    return result


def parse_json_in_dict(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def main():
    # shell_syn_flood_attack = ShellCommandsTranslator(
    #     port,
    #     ip,
    #     flood_flag=syn_flood_flag,
    #     count_packets=count_packets
    # ).to_shell_command()
    # print(shell_syn_flood_attack)
    #
    # start_syn_flood_attack_executor = ShellCommandsExecutor(shell_syn_flood_attack)
    # report_syn_flood_attack = start_syn_flood_attack_executor.execute()
    # status_syn_flood_attack = check_success_syn_flood_attack(report_syn_flood_attack)
    # print(status_syn_flood_attack)
    data = parse_json_in_dict('data.json')
    result = NmapReportTranslator(data).to_tcp()


if __name__ == '__main__':
    main()
