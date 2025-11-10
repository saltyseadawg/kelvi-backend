import json

import marisa_trie


GRAMBLE_TAMIL_FILE = "app/morphology/glosser/gramble_tamil_output.json"


class Glosser:
    """
    Provides the gramatical gloss.
    Use trie to store text for gloss because of efficient string searching when looking for longest to shortest substrings.
    https://en.wikipedia.org/wiki/Trie
    """

    def __init__(self, filepath=GRAMBLE_TAMIL_FILE):
        self.gloss_dict = {}
        with open(filepath, "r") as file:
            data = json.load(file)
            for item in data:
                self.gloss_dict[item["text"]] = item["gloss"]
        self.trie = marisa_trie.Trie(self.gloss_dict.keys())

    def find_morphemes(self, word):
        inTrie = False
        word_len = len(word)
        suffix = ""
        lemma = ""

        for i in range(1, word_len):
            suffix = word[i:]
            inTrie = suffix in self.trie
            if inTrie:
                lemma = word[:i]
                morphemes = {"suffix": suffix, "lemma": lemma}
                return morphemes
        return None

    def gloss_suffix(self, word, lemma=""):
        """
        search backwards on the input word, searching for the suffixes from Gramble
        making sure to search from largest suffix string to shortest
        and making sure the entire word isn’t just suffix
        if the word is entirely suffix, then remove the lemma and have the remainder run through Gramble
        or just retain stemmer as something to run it through as an edge case
        """
        inTrie = False
        suffix = word
        if word in self.trie:
            suffix = word.replace(lemma, "")

        for i in range(1, len(suffix)):
            substr = suffix[i:]
            inTrie = substr in self.trie
            if inTrie:
                break

        if inTrie:
            gloss = (substr, self.gloss_dict[substr])
            return gloss
        return None

    def get_gloss(self, text):
        return self.gloss_dict.get(text, None)
