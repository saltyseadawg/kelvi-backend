import unittest

from app.romanizer.TamilRomanizer import TamilRomanizer
from app.models import InputWord, TamilForm, Gloss


class TestRomanizer(unittest.TestCase):
    def setUp(self):
        self.romanizer = TamilRomanizer("tamil-roman-mapping.csv")

    def test_romanization(self):
        word = "சாவி"
        expected = "cha:vi"
        romanized = self.romanizer.romanize(word)

        word = "ஈரம்"
        expected = "i:ram"
        romanized = self.romanizer.romanize(word)

        word = "மரத்தில்"
        expected = "maraththil"
        romanized = self.romanizer.romanize(word)

        word = "பக்கம்"
        expected = "pakkam"
        romanized = self.romanizer.romanize(word)

        word = "ஔவையார்"
        expected = "owvaiya:r"
        romanized = self.romanizer.romanize(word)

        word = "நடப்போம்"
        expected = "naṭappo:m"
        romanized = self.romanizer.romanize(word)

        word = "தமிழ்"
        expected = "thamizh"
        romanized = self.romanizer.romanize(word)

        word = "பண்ணிட்டேன்"
        expected = "paṇṇiṭṭe:n"
        romanized = self.romanizer.romanize(word)

        assert romanized == expected

        word = "உங்களுடைய"
        expected = "ungkaḷuṭaiya"
        romanized = self.romanizer.romanize(word)

        assert romanized == expected

    def test_normalization(self):
        word = "போ"
        expected = "போ"
        assert self.romanizer.normalize(word) == expected

        word = "கௌரவா"
        expected = "கௌரவா"
        assert self.romanizer.normalize(word) == expected

        word = "கொள்"
        expected = "கொள்"
        assert self.romanizer.normalize(word) == expected

    def test_romanize_query(self):
        word = InputWord(
            user_input="மேய்ந்தன",
            root=TamilForm(tamil="மேய்"),
            suffixal_material=Gloss(display="ந்தன", gloss="they did"),
        )
        self.romanizer.romanize_query(word)

        assert word.root.romanization == "me:y"
        assert word.romanization == "me:ynthana"
        assert word.suffixal_material.romanization == "nthana"
