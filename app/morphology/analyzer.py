import stanza

from app.models import InputWord, TamilForm
from app.morphology import lemmatizer, stemmer, affixes

def analyze_word(word: str, pipeline=None):
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
    
    stanza_result = lemmatizer.process_word(pipeline, word)
    lemma = stanza_result.lemma
    stem = lemma

    if lemma != word:
        stem = stemmer.stem_word(word)
    prefix = affixes.get_prefix(word, stem)
    suffix = affixes.get_suffix(word, stem)

    return InputWord(
        user_input=word,
        root=TamilForm(tamil=lemma),
        prefixal_material=prefix,
        suffixal_material=suffix
    )


    


