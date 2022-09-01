class ListTranslator:
    def __init__(self, item_translator):
        self.item_translator = item_translator

    def from_json(self, items: list) -> list:
        return [
            self.item_translator.from_json(item)
            for item
            in items
        ]
