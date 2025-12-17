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
        suffixal_material=Gloss(display="ந்தேன்", gloss="I did", raw="ந்தேன்"),
    )
    assert expected == result


def test_analyze_word_gramble(glosser_obj):
    word = "மெய்ந்தன"
    result = analyzer.analyze_word_gramble(word, glosser_obj)

    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil="மெய்"),
        suffixal_material=Gloss(display="ந்தன", gloss="they did", raw="ந்தன"),
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

def test_analyze_word_add_back_no_change(glosser_obj):
    word = "போட்டான்"
    result = analyzer.analyze_word_gramble(word, glosser_obj)
    analyzer.analyze_word_add_back(result, glosser_obj)
    
    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil="போடு"),
        suffixal_material=Gloss(
            display="ட்டான்",
            gloss="he did",
            raw="ட்டான்"
        ),
    )
    assert expected == result

def test_analyze_word_add_back_no_suffix(glosser_obj):
    word = "hello"
    result = analyzer.analyze_word_gramble(word, glosser_obj)
    analyzer.analyze_word_add_back(result, glosser_obj)
    
    expected = InputWord(
        user_input=word,
        root=TamilForm(tamil="hello"),
        suffixal_material=None,
    )
    assert expected == result


# def test_analyze_word_add_back_change(glosser_obj):
#     word = "அவனுக்கு"
#     result = analyzer.analyze_word_gramble(word, glosser_obj)
#     analyzer.analyze_word_add_back(result, glosser_obj)
    
#     expected = InputWord(
#         user_input=word,
#         root=TamilForm(tamil="அவன்"),
#         suffixal_material=Gloss(
#             display="க்கு",
#             gloss="he did",
#             raw="ுக்கு"
#         ),
#     )
#     assert expected == result
