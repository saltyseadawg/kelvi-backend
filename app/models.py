from pydantic import BaseModel
from typing import Optional
import abc

class DictEntry(BaseModel, abc.ABC):
    id: int
    lang: str
    pos: Optional[str] = None
    primary_definition: str
    secondary_definition: Optional[str] = None
    tertiary_definition: Optional[str] = None
    examples: Optional[list[str]] = None
    source: Optional[str] = None
    
class InputWord(BaseModel, abc.ABC):
    headword: str
    romanization: Optional[str]=None
    root: str
    root_definitions: list[DictEntry]
    secondary_root_definitions: Optional[list[DictEntry]] # stretch goal to segment compound words; for now want to just capture them unsegmented
    prefixal_material: Optional[str]=None # to get passed to gramble for parsing
    suffixal_material: Optional[str]=None # to get passed to gramble for parsing
    pos: list[DictEntry] # for SS to think about, bc root and derived word can have diff POS. can leave for now
    
    @abc.abstractmethod
    def set_romanization(self):
        pass

class TamilHeadword(InputWord):
    def set_romanization(self):
        pass