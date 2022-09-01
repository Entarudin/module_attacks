class ResultAttackService:
    def __check_success_syn_flood_attack(self, report: str) -> bool:
        list_report = report.split('\n')[1:]
        flag = ''
        for data in list_report:
            for item in data.split(' '):
                if 'flags' in item:
                    chunks = item.split('=')
                    flag = chunks[1]

        result = True if flag == 'SA' else False
        return result

    def __check_success_udp_flood_attack(self, report: str) -> bool:
        list_report = report.split('\n')
        list_icmp_responses = []

        for data in list_report:
            if "ICMP Port Unreachable" in data:
                list_icmp_responses.append(data)
        result = True if len(list_icmp_responses) != 0 else False
        return result

    def check_status_attack(self, type_attack: str, report: str) -> bool:
        if type_attack == 'syn_flood':
            return self.__check_success_syn_flood_attack(report)
        if type_attack == 'udp_flood':
            return self.__check_success_udp_flood_attack(report)
