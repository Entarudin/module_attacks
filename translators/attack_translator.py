from models import Attack


class AttackTranslator:
    def __init__(self, target_translator):
        self.target_translator = target_translator

    def to_dict(self, model: Attack) -> dict:
        return {
            "target": self.target_translator.to_dict(model.target),
            "status": model.status
        }
