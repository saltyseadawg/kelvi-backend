import unittest
from app.morphology.glosser.Glosser import Glosser
from app.models import Gloss


class TestGlosser(unittest.TestCase):
    def setUp(self):
        self.glosser = Glosser()

    def test_gloss_suffix(self):
        word = "மரங்களைப்"
        expected = Gloss(display="களை", gloss="plural")
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss

        word = "குடித்திருக்கமாட்டேன்"
        expected = Gloss(display="ிருக்க-மாட்டேன்", gloss="I wouldn't have done")
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss

        word = "நடக்கட்டும்"
        expected = Gloss(display="ட்டும்", gloss="let them/her/him/it do it")
        gloss = self.glosser.gloss_suffix(word)

        assert expected == gloss
