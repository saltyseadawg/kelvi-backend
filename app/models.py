from pydantic import BaseModel
from typing import Optional
import abc

class DictEntry(BaseModel, abc.ABC):
    id: int
    lang: str
    pos: Optional[str] = None
    definitions: list[str]
    examples: Optional[list[int]] = None # list of ids that reference an example containing the word (examples would be in their own table in a DB)
    source: Optional[str] = None
    
class InputWord(BaseModel, abc.ABC):
    user_input = str
    romanization: Optional[str]=None
    root: str
    root_definition: DictEntry 
    secondary_root_definitions: Optional[list[DictEntry]] # stretch goal to segment compound words; for now want to just capture them unsegmented
    prefixal_material: Optional[str]=None # to get passed to gramble for parsing
    suffixal_material: Optional[str]=None # to get passed to gramble for parsing
    infixal_material: Optional[str]=None # not relevant for Tamil
    pos: list[DictEntry] # for SS to think about, bc root and derived word can have diff POS. can leave for now
    
    @abc.abstractmethod
    def set_romanization(self):
        pass
    
class TamilHeadword(InputWord):
    def set_romanization(self):
        pass