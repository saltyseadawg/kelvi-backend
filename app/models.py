from pydantic import BaseModel
from typing import Optional
import abc

    

class TamilForm(BaseModel, abc.ABC): # any Tamil form/string has to have the form in Tamil orthography and optionally romanization
    tamil: str
    romanization: Optional[str] = None # this will eventually call on the romanization function

class DictEntry(BaseModel, abc.ABC):
    id: int
    lang: str
    pos: Optional[str] = None
    romanization: Optional[str] = None
    definitions: list[str]
    centamil_koduntamil_equiv: Optional[TamilForm] = None # some words have entirely different forms in the formal (centamil) vs informal (koduntamil) registers, and the dictionary seems to track that
    related_forms: Optional[list[TamilForm]] = None # often related to centamil_koDuntamil, or perhaps common conjugations of the stem
    examples: Optional[list[int]] = None # list of ids that reference an example containing the word (examples would be in their own table in a DB)
    source: Optional[str] = None
    
class InputWord(BaseModel, abc.ABC):
    user_input: str
    romanization: Optional[str]=None
    root: TamilForm
    root_definition: DictEntry # stretch goal to segment compound words; for now want to just capture them unsegmented
    prefixal_material: Optional[str]=None # to get passed to gramble for parsing
    suffixal_material: Optional[str]=None # to get passed to gramble for parsing
    infixal_material: Optional[str]=None # not relevant for Tamil


    @abc.abstractmethod
    def set_romanization(self):
        pass
    
class TamilHeadword(InputWord):
    def set_romanization(self):
        pass