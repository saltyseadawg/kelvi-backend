import Stemmer


def stem_word(word: str, lang: str = "tamil") -> str:
    """Will need to modify the stemmer so that it stems according to
    our pipeline needs i.e. சாப்பிட்டேன் -> சாப்பிட் instead of சாப்பிடு
    """
    stemmer = Stemmer.Stemmer(lang)
    stem = stemmer.stemWord(word)
    return stem
