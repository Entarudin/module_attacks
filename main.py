import json

from start_attacks import start_attacks

def main():
    attacks = start_attacks()
    with open("data/result.json", 'w') as json_file:
        json.dump(attacks, json_file, indent=2)


if __name__ == '__main__':
    main()