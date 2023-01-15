import json


class JsonService:
    def parse_in_dict(self, filename: str) -> dict:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    def save_dict_in_file(self, filename: str, presented: dict):
        with open(filename, 'w') as json_file:
            json.dump(presented, json_file, indent=2)
