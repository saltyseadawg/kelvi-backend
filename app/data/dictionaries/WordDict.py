from app.models import TamilDictEntry, TamilForm, InputWord

import json


class WordDict:
    """Don't want to keep opening the dictionary file.
    Eventually this will be obselete if we ever implement a database.
    """

    def __init__(self, dict_filepath: str = "mcalpin"):
        dict_path = f"app/data/dictionaries/{dict_filepath}.json"
        with open(dict_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def search_word(self, word: str):
        result = None
        if word in self.data:
            word_data = self.data[word]
            result = InputWord(
                user_input=word,
                root=TamilForm(tamil=word),
                root_definition=TamilDictEntry(**word_data),
            )

        return result
