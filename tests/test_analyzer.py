from app.morphology import analyzer

from app.models import InputWord, TamilForm

import pytest
import stanza


@pytest.fixture
def stanza_pipeline():
    return stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        download_method="reuse_resources",
    )


def test_analyze_word(stanza_pipeline):
    word = "இருந்தேன்"
    result = analyzer.analyze_word(word, stanza_pipeline)

    expected = InputWord(
        user_input=word, root=TamilForm(tamil="இரு"), suffixal_material="ந்தேன்"
    )
    assert expected == result
