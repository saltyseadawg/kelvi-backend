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
    


if __name__ == '__main__':
    unittest.main()