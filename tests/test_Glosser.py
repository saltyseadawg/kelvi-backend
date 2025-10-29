import unittest
from app.morphology.glosser.Glosser import Glosser


class TestGlosser(unittest.TestCase):
    def setUp(self):
        self.glosser = Glosser()

    def test_gloss_suffix(self):
        word = "பண்ணாதே"
        expected = ("ாதே", "[don'tdoit]")
        gloss = self.glosser.gloss_suffix(word)
        assert gloss == expected
