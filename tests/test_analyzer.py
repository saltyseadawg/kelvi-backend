from app.morphology import analyzer
from app.morphology.glosser.Glosser import Glosser
from app.models import InputWord, TamilForm, Gloss

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
    result = analyzer.analyze_word_stanza(word, stanza_pipeline)

    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil="இரு"),
        suffixal_material=Gloss(display="ந்தேன்", gloss="I did"),
    )
    assert expected == result


def test_analyze_word_gramble(glosser_obj):
    word = "மெய்ந்தன"
    result = analyzer.analyze_word_gramble(word, glosser_obj)

    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil="மெய்"),
        suffixal_material=Gloss(display="ந்தன", gloss="they did"),
    )
    assert expected == result


def test_analyze_word_gramble_no_lemma(glosser_obj):
    word = "hello"
    result = analyzer.analyze_word_gramble(word, glosser_obj)

    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil=word),
        suffixal_material=None,
    )
    assert expected == result

def test_analyze_word_stanza_no_suffix(stanza_pipeline):
    word = "நீந்து"
    result = analyzer.analyze_word_stanza(word, stanza_pipeline)

    expected = InputWord(
            user_input=word,
            root=TamilForm(tamil=word),
            suffixal_material=None,
        )
    assert expected == result