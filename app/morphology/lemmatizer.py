"""

"""
def process_word(pipeline, word: str):
    """
    The lemmatization is handled by the Stanford NLP pipeline and 
    also returns other information (i.e. POS).
    """
    doc = pipeline(word)
    word = get_first_word_from_pipeline(doc)
    return word

def lemmatize_word(pipeline, word: str):
    result = process_word(pipeline, word)
    return result.lemma

def get_first_word_from_pipeline(doc) -> dict:
    for s in doc.sentences:
        for w in s.words:
            return w