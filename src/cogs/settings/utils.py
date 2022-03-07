class Utils:

    @staticmethod
    def snake_case_to_sentence(string: str) -> str:
        return string.replace("_", " ").capitalize()
