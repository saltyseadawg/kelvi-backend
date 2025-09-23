from app.morphology import lemmatizer

import pytest
import stanza

@pytest.fixture
def stanza_pipeline():
    return stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        download_method="reuse_resources",
    )

def test_lemmatize_word(stanza_pipeline):
    word = "தூங்கினாள்"
    expected = "தூங்கு"
    lemma = lemmatizer.lemmatize_word(stanza_pipeline, word)
    assert expected == lemma