import unittest
from app.morphology.glosser.Glosser import Glosser
from app.models import Gloss


class TestGlosser(unittest.TestCase):
    def setUp(self):
        self.glosser = Glosser()

    def test_gloss_suffix(self):
        word = "மரங்களைப்"
        expected = Gloss(display="களை", gloss=["plural"], raw="களைப்")
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss

        word = "குடித்திருக்கமாட்டேன்"
        expected = Gloss(
            display="ிருக்க-மாட்டேன்", gloss=["I wouldn't have done"], raw="த்திருக்கமாட்டேன்"
        )
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss

        word = "நடக்கட்டும்"
        expected = Gloss(
            display="ட்டும்", gloss=["let them/her/him/it do it"], raw="க்கட்டும்"
        )
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss

    def test_get_gloss_multiple_defns(self):
        suffix = "ும்"
        result = self.glosser.get_gloss(suffix)
        expected = Gloss(
            display="ும்",
            gloss=set(["and/also", "thing that will be doing", "it will"]),
            raw="ும்",
            romanization=None,
        )

        assert expected == result

    def test_add_back(self):
        stem = "பாட"
        suffix = "ினேன்"
        expected = "பாடு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        # doesn't work rn, will be fixed after migrating to db
        # stem = "பண்ண"
        # suffix = "ட்டும்"
        # expected = "பண்ணு"

        # result = self.glosser.add_back(suffix, stem)
        # assert expected == result

        stem = "தூங்க"
        suffix = "லாம்"
        expected = "தூங்கு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "அழ"
        suffix = "ாதே"
        expected = "அழு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "விழ"
        suffix = "ுங்கள்"
        expected = "விழு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "தூங்க"
        suffix = "ேன்"
        expected = "தூங்கு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "நட"
        suffix = "க்கிறார்"
        expected = "நட"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "சாப்பி"
        suffix = "ட்டிருந்தால்"
        expected = "சாப்பிடு"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result

        stem = "செ"
        suffix = "ஞ்சிருந்தும்"
        expected = "செய்"

        result = self.glosser.add_back(suffix, stem)
        assert expected == result
