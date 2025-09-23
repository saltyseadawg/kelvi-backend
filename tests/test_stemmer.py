from app.morphology import stemmer

def test_stem_word():
    word = 'இருந்தேன்' 
    stem = stemmer.stem_word(word)
    expected = 'இரு'
    assert stem == expected
    