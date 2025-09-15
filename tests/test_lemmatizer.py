import stanza
import unittest

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nlp = stanza.Pipeline(lang='ta', processors='tokenize,mwt,pos,lemma')

class TestStringMethods(unittest.TestCase):

    def test_word(self):
        nlp = stanza.Pipeline(lang='ta', processors='tokenize,mwt,pos,lemma')
        doc = nlp('அறிந்துகொண்டேன்')
        for sent in doc.sentences:
            for word in sent.words:
                root = word.lemma
        self.assertEqual(root, 'அறி')

    def test_imperative(self):
        nlp = stanza.Pipeline(lang='ta', processors='tokenize,mwt,pos,lemma')
        imperatives = {'பண்ணு': 'பண்ணு',
        'பண்ணாதே': 'பண்ணு',
        'பண்ணுங்கள்': 'பண்ணு',
        'பண்ணாதீர்கள்': 'பண்ணு',
        'பண்ணேன்': 'பண்ணு',
        'பண்ணாதேயேன்': 'பண்ணு',
        'பண்ணுங்களேன்': 'பண்ணு',
        'பண்ணாதீர்களேன்': 'பண்ணு',
        'வாயேன்': 'வா'}
        for imperative in imperatives:
            doc = nlp(imperative)
            for sent in doc.sentences:
                for word in sent.words:
                    root = word.lemma
            self.assertEqual(root, imperatives[imperative])
    


if __name__ == '__main__':
    unittest.main()