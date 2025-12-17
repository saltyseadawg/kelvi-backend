from app.models import InputWord, TamilForm
from app.morphology import stanza_utils
from app.morphology.glosser.Glosser import Glosser

import stanza


def analyze_word_stanza(word: str, pipeline=None, glosser=None):
    """
    Saapitten
    Lemma: sappidu
    Suffix: tten
    Stemmer: saappi

    Put word in lemmatizer
    Search for lemma in dictionary to return meaning, and return lemma as the "root"
    Put whole word in stemmer
    Search for the output of the stemmer in the input word, to split out the prefixal and suffixal material
    Run the prefixal material through grambke
    Run the suffixal through Gramble
    """
    if pipeline is None:
        pipeline = stanza.Pipeline(
            lang="ta",
            processors="tokenize,mwt,pos,lemma",
            download_method="reuse_resources",
        )

    if glosser is None:
        glosser = Glosser()

    stanza_result = stanza_utils.process_word(pipeline, word)
    lemma = stanza_result.lemma
    gloss = None
    if word != lemma:
        gloss = glosser.gloss_suffix(word, lemma)

    return InputWord(
        user_input=word,
        root=TamilForm(tamil=lemma),
        suffixal_material=gloss,
    )


def analyze_word_gramble(word: str, glosser=None):
    morphemes = glosser.find_morphemes(word)
    lemma = word
    gloss = None

    if morphemes:
        lemma = morphemes["lemma"]
        suffix = morphemes["suffix"]
        if word != lemma:
            gloss = glosser.get_gloss(suffix)

    return InputWord(
        user_input=word,
        root=TamilForm(tamil=lemma),
        suffixal_material=gloss,
    )

def analyze_word_add_back(input_word: InputWord, glosser=None):
    if glosser is None:
        glosser = Glosser()
    new_lemma = glosser.add_back(input_word.suffixal_material.raw, input_word.root.tamil)
    input_word.root.tamil = new_lemma
