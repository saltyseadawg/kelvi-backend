from app.routers import e2e_testing
from app.morphology import analyzer
from app.morphology.glosser.Glosser import Glosser
from app.models import InputWord, TamilForm, Gloss
from app.data.dictionaries.WordDict import WordDict

import unittest

from app.lang_mappings.converter import Converter, Romanizer

import pytest
import stanza


class TestProcessInputWord(unittest.TestCase):
    def setUp(self):
        self.romanizer = Romanizer("tamil", "romanization")
        self.tamilizer = Converter("romanization", "tamil")
        self.stanza_pipeline = stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        # uncomment for local development
        # download_method="reuse_resources"
        download_method=None,
    )
        self.glosser = Glosser
        tamil_dicts = {}
        dict_names = ["mcalpin", "wiktionary"]
        for name in dict_names:
            tamil_dicts[name] = WordDict(name)
        self.tamil_dicts = tamil_dicts


    def test_process_input_word(self):
        sample_string = InputWord(user_input="அம்மா")
        word_data = e2e_testing.process_input_word(word_data=sample_string, tamilizer=self.tamilizer, romanizer=self.romanizer, 
        stanza_pipeline=self.stanza_pipeline, tamil_dicts=self.tamil_dicts, glosser=self.glosser)
        expected_user_input = "அம்மா"
        expected_romanization = "amma:"
        expected_root = "அம்மா"
        expected_prefixal_material = None
        expected_suffixal_material = None
        assert word_data.user_input == expected_user_input
        assert word_data.root.romanization == expected_romanization
        assert word_data.root.tamil == expected_root
        assert word_data.prefixal_material == expected_prefixal_material
        assert word_data.suffixal_material == expected_suffixal_material
