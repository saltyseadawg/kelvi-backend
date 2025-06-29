from pydantic import BaseModel
from typing import Optional
import abc

class DictEntry(BaseModel, abc.ABC):
    id: int
    lang: str
    pos: Optional[str] = None
    definition: str
    examples: Optional[list[str]] = None
    source: Optional[str] = None
    
class HeadWord(BaseModel, abc.ABC):
    headword: str
    romanization: Optional[str]=None
    definitions: list[DictEntry]
    
    @abc.abstractmethod
    def set_romanization(self):
        pass

class TamilHeadword(HeadWord):
    def set_romanization(self):
        pass