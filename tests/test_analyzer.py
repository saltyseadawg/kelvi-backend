from app.morphology import analyzer
from app.morphology.glosser.Glosser import Glosser
from app.models import Gloss

import pytest
import stanza


@pytest.fixture
def stanza_pipeline():
    return stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        download_method="reuse_resources",
    )


@pytest.fixture
def glosser_obj():
    return Glosser()


def test_analyze_word_stanza(stanza_pipeline):
    word = "இருந்தேன்"
    lemma, suffix = analyzer.analyze_word_stanza(word, stanza_pipeline)

    expected_lemma = "இரு"
    expected_suffix = Gloss(display="ந்தேன்", gloss=["I did"], raw="ந்தேன்")

    assert expected_lemma == lemma
    assert expected_suffix == suffix


def test_analyze_word_gramble(glosser_obj):
    word = "மெய்ந்தன"
    lemma, suffix = analyzer.analyze_word_gramble(word, glosser_obj)

    expected_lemma = "மெய்"
    expected_suffix = Gloss(display="ந்தன", gloss=["they did"], raw="ந்தன")

    assert expected_lemma == lemma
    assert expected_suffix == suffix


def test_analyze_word_gramble_no_lemma(glosser_obj):
    word = "hello"
    lemma, suffix = analyzer.analyze_word_gramble(word, glosser_obj)

    expected_lemma = "hello"
    expected_suffix = None

    assert expected_lemma == lemma
    assert expected_suffix == suffix


def test_analyze_word_stanza_no_suffix(stanza_pipeline):
    word = "நீந்து"
    lemma, suffix = analyzer.analyze_word_stanza(word, stanza_pipeline)

    expected_lemma = "நீந்து"
    expected_suffix = None

    assert expected_lemma == lemma
    assert expected_suffix == suffix


def test_analyze_word_add_back_no_change(glosser_obj):
    word = "போட்டான்"
    stem, suffix = analyzer.analyze_word_gramble(word, glosser_obj)
    lemma = analyzer.analyze_word_add_back(stem, suffix, glosser_obj)

    expected = "போடு"
    assert expected == lemma


def test_analyze_word_add_back_no_suffix(glosser_obj):
    word = "hello"
    stem, suffix = analyzer.analyze_word_gramble(word, glosser_obj)
    lemma = analyzer.analyze_word_add_back(stem, suffix, glosser_obj)

    expected = "hello"
    assert expected == lemma
