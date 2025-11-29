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

