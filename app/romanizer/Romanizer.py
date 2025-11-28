import csv
from pathlib import Path
from abc import ABC, abstractmethod


MAPPING_DIR = 'app/romanizer/mappings'

class Romanizer(ABC):
    def __init__(self, mapping_file:str):
        self.mapping = self.mapping_to_dict(mapping_file)

    @abstractmethod
    def mapping_to_dict(self):
        pass

    @abstractmethod
    def romanize(self):
        pass

class TamilRomanizer(Romanizer):
    
    def mapping_to_dict(self, filename: str) -> dict:
        filepath = Path(MAPPING_DIR, filename)
        map_dict = {}
        with open(filepath) as file:
            reader = csv.DictReader(file, delimiter=',')
            # skip header
            next(reader, None)
            for row in reader:
                key = row['tamil']
                val = row['roman']
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

