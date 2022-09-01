import json


class JsonService:
    def parse_in_dict(self, filename: str) -> dict:
        with open(filename) as json_file:
            data = json.load(json_file)
        return data

    def write_in_file(self, filename: str, content):
        with open(filename, 'w') as json_file:
            dictionary = {
                "content": content
            }

            json.dump(dictionary, json_file, indent=2)
