import json
import re

from app.models import Gloss

import marisa_trie


GRAMBLE_TAMIL_FILE = "app/morphology/glosser/gramble_tamil_output.json"


class Glosser:
    """
    Provides the gramatical gloss.
    Use trie to store text for gloss because of efficient string searching when looking for longest to shortest substrings.
    https://en.wikipedia.org/wiki/Trie
    """

    BRACKETS_RE = re.compile(r"[\[\]]")
    NULL_RE = re.compile(r"null$")
    SEP_HYPHEN_RE = re.compile(r"-(?=[A-Za-z(])")

    def __init__(self, filepath=GRAMBLE_TAMIL_FILE):
        self.gloss_dict = {}
        with open(filepath, "r") as file:
            data = json.load(file)
            for item in data:
                self.gloss_dict[item["text"]] = {
                    "display": self._clean_text(item["display"]),
                    "gloss": self._clean_text(item["gloss"]),
                }
                add_back = item.get('add-back')
                if add_back:
                    self.gloss_dict[item["text"]]["add-back"] = add_back
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
        gloss = None
        if word in self.trie:
            suffix = word.replace(lemma, "")

        for i in range(1, len(suffix)):
            substr = suffix[i:]
            inTrie = substr in self.trie
            if inTrie:
                break

        if inTrie:
            gloss = self.get_gloss(substr)
        return gloss

    def get_gloss(self, text):
        item = self.gloss_dict.get(text, None)
        gloss = None
        if item:
            gloss = Gloss(
                display=item['display'],
                gloss=item['gloss'],
                raw=text,
            )
        
        return gloss

    def _clean_text(self, s: str) -> str:
        """Generated with ChatGPT"""
        s = self.BRACKETS_RE.sub("", s)
        s = self.NULL_RE.sub("", s)
        s = self.SEP_HYPHEN_RE.sub(" ", s)
        return s.strip()

    def add_back(self, suffix, stem):
        """Attempt to add back part of lemma potentially 
        removed due to morphophonological transformations.
        """
        new_stem = stem
        if suffix in self.trie:
            to_add = self.gloss_dict[stem].get('add-back', '')
            new_stem += to_add
        
        return new_stem
    
    
    
