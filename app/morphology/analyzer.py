from app.models import InputWord, TamilForm
from app.morphology import lemmatizer, stemmer, affixes
from app.morphology.glosser.Glosser import Glosser

import stanza


def analyze_word(word: str, pipeline=None, glosser=None):
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

    stanza_result = lemmatizer.process_word(pipeline, word)
    lemma = stanza_result.lemma

    gloss_result = glosser.gloss_suffix(word, lemma)
    suffix = None
    suffix_gloss = None
    if gloss_result is not None:
        suffix = gloss_result[0]
        suffix_gloss = gloss_result[1]
    
    
    # if lemma != word:
    #     stem = stemmer.stem_word(word)
    # prefix = affixes.get_prefix(word, stem)
    # suffix = affixes.get_suffix(word, stem)
    return InputWord(
        user_input=word,
        root=TamilForm(tamil=lemma),
        suffixal_material={'text':suffix, 'gloss': suffix_gloss}
    )
