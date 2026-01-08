from pydantic import BaseModel
from typing import Optional
import abc


class TamilForm(
    BaseModel
):  # any Tamil form/string has to have the form in Tamil orthography and optionally romanization
    tamil: str
    romanization: str | None = (
        None  # this will eventually call on the romanization function? maybe we won't even need to store it?
    )


class DictEntry(BaseModel, abc.ABC):
    pos: str | None = None
    definitions: list[str]
    examples: Optional[list] = (
        None  # list of ids that reference an example containing the word (examples would be in their own table in a DB)
    )
    source: Optional[str] = None


class TamilDictEntry(DictEntry):
    romanization: str | None = None
    centamil_koduntamil_equiv: Optional[TamilForm] = (
        None  # some words have entirely different forms in the formal (centamil) vs informal (koduntamil) registers, and the dictionary seems to track that
    )
    related_forms: Optional[list[TamilForm]] = (
        None  # often related to centamil_koDuntamil, or perhaps common conjugations of the stem
    )


class Gloss(BaseModel):
    display: str
    gloss: list[str]
    raw: str
    romanization: str | None = None


class InputWord(BaseModel):
    user_input: str
    processed_input: TamilForm | None = None
    romanization: str | None = None
    root: TamilForm | None = None
    root_definition: list[
        DictEntry
    ] = []  # stretch goal to segment compound words; for now want to just capture them unsegmented
    prefixal_material: Gloss | None = None  # to get passed to gramble for parsing
    suffixal_material: Gloss | None = None  # to get passed to gramble for parsing
    infixal_material: Gloss | None = None  # not relevant for Tamil
