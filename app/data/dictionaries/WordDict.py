from app.models import TamilDictEntry, InputWord

import json


class WordDict:
    """Don't want to keep opening the dictionary file.
    Eventually this will be obselete if we ever implement a database.
    """

    def __init__(self, dict_filepath: str = "mcalpin"):
        dict_path = f"app/data/dictionaries/{dict_filepath}.json"
        with open(dict_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def search_word(self, user_input: InputWord) -> bool:
        root = user_input.root.tamil
        isFound = False
        if root in self.data:
            word_data = self.data[root]
            user_input.root_definition.append(TamilDictEntry(**word_data))
            isFound = True
        return isFound
