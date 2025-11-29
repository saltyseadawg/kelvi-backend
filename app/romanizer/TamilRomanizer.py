import re
import csv
from pathlib import Path

from app.romanizer.Romanizer import MAPPING_DIR, Romanizer


class TamilRomanizer(Romanizer):
    
    def __init__(self, mapping_file):
        super().__init__(mapping_file)
        self.normal_mapping = {
            "\u0bc7\u0bbe": "\u0bcb",
            "\u0bc6\u0bbe": "\u0bca",
            "\u0bc6\u0BD7": "\u0BCC"
        }

    def mapping_to_dict(self, filename: str) -> dict:
        filepath = Path(MAPPING_DIR, filename)
        map_dict = {}
        with open(filepath) as file:
            reader = csv.DictReader(file, delimiter=',')
            # skip header
            next(reader, None)
            for row in reader:
                key = row['from']
                val = row['to']
                map_dict[key] = val
        return map_dict

    def romanize(self, text: str) -> str:
        romanized = ''
        length = len(text)

        if length == 0:
            pass
        elif length == 1:
            romanized = self.mapping.get(text, '')
        else:
            i = 0
            while i < length:
                letter = text[i]
                print(text[i])
                if i + 2 <= length:
                    cluster = letter + text[i+1]
                    print(cluster)
                    if cluster in self.mapping:
                        romanized += self.mapping[cluster]
                        i += 2
                        continue
                romanized += self.mapping[letter]
                i += 1
        return romanized

    def normalize(self, text: str) -> str:
        """Normalize unicode characters."""
        pattern = re.compile("|".join(map(re.escape, self.normal_mapping.keys())))
        result = pattern.sub(lambda m: self.normal_mapping[m.group(0)], text)
        return result