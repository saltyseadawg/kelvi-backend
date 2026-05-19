import re

from app.models import TamilForm, InputWord

from fastapi import APIRouter, HTTPException, Request
from app.morphology import analyzer

router = APIRouter()

    #helper function
def read_word(query: str, debug: bool):
    word_data = InputWord(user_input=query.strip())
    # we only handle first word in a query for now
    first_word = word_data.user_input.split()[0]
    # unable to handle any hybrid Tamil + romanization words
    if re.search("[a-zA-Z]", word_data.user_input):
        tamil = app.state.tamilizer.convert(first_word)
        tamil = re.sub("[a-zA-Z]", "", tamil)
        roman = app.state.romanizer.convert(tamil)
        word_data.processed_input = TamilForm(tamil=tamil, romanization=roman)
    else:
        word_data.processed_input = TamilForm(
            tamil=first_word,
            romanization=app.state.romanizer.convert(first_word),
        )

    debug_material = {"stanza_lemma":"none", "suffix_stripped_lemma":"none", 
    "add_back_lemma":"none", "raw_suffix":"none"}
    # try lemmatizer
    lemma, suffixal_material = analyzer.analyze_word_stanza(
        word_data.processed_input.tamil, pipeline=app.state.stanza_pipeline
    )
    debug_material["stanza_lemma"] = lemma
    defns = []
    tamil_dicts = app.state.tamil_dicts
    for d in tamil_dicts.values():
        defns.extend(d.search_word(lemma))
    if not defns:
        # try using gramble to find suffix
        lemma, suffixal_material = analyzer.analyze_word_gramble(
            lemma, app.state.glosser
        )
        debug_material["suffix_stripped_lemma"] = lemma
        for d in tamil_dicts.values():
            defns.extend(d.search_word(lemma))
    if not defns:
        # try add back to find lemma
        lemma = analyzer.analyze_word_add_back(
            lemma, suffixal_material, app.state.glosser
        )
        debug_material["add_back_lemma"] = lemma
        for d in tamil_dicts.values():
            defns.extend(d.search_word(lemma))
    if not defns:
        raise HTTPException(status_code=404, detail="Word not found")
    word_data.root_definition = defns
    word_data.root = TamilForm(
        tamil=lemma, romanization=app.state.romanizer.convert(lemma)
    )
    if suffixal_material:
        suffixal_material.romanization = app.state.romanizer.convert(
            suffixal_material.display
        )
        word_data.suffixal_material = suffixal_material
        debug_material["raw_suffix"] = suffixal_material.raw

    if not debug:
        return word_data
    if debug:
        return debug_material