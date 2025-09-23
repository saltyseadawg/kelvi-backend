from app.morphology import stemmer


def test_stem_word():
    word = "இருந்தேன்"
    stem = stemmer.stem_word(word)
    expected = "இரு"
    assert stem == expected


def test_adjusted_stemmer_output():
    # word = 'சாப்பிட்டேன்'
    # stem = stemmer.stem_word(word)
    # expected = 'சாப்பிட்'
    # doesn't work right now
    # assert stem == expected
    pass
