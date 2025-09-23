import Stemmer

def stem_word(word: str, lang: str="tamil") -> str:
    stemmer = Stemmer.Stemmer(lang)
    stem = stemmer.stemWord(word)
    return stem
