from pydantic import BaseModel
from typing import Optional
import abc

class DictEntry(BaseModel, abc.ABC):
    id: int
    lang: str
    pos: Optional[str] = None
    definition: str
    examples: Optional[list[str]] = None
    source: Optional[str]
    
class HeadWord(BaseModel, abc.ABC):
    headword: str
    definitions: list[DictEntry]
    romanization: str

    @abc.abstractmethod
    def __init__(self, x, y):
        pass
    
    @abc.abstractmethod
    def set_romanization(self):
        pass
