import unittest

from app.lang_mappings.converter import Converter

class TestRomanization(unittest.TestCase):
    def setUp(self):
        self.romanizer = Converter('tamil', 'romanization')

    def test_romanization(self):
        word = "சாவி"
        expected = "cha:vi"
        romanized = self.romanizer.convert(word)

        word = "ஈரம்"
        expected = "i:ram"
        romanized = self.romanizer.convert(word)

        word = "மரத்தில்"
        expected = "maraththil"
        romanized = self.romanizer.convert(word)

        word = "பக்கம்"
        expected = "pakkam"
        romanized = self.romanizer.convert(word)

        word = "ஔவையார்"
        expected = "owvaiya:r"
        romanized = self.romanizer.convert(word)

        word = "நடப்போம்"
        expected = "naṭappo:m"
        romanized = self.romanizer.convert(word)

        word = "தமிழ்"
        expected = "thamizh"
        romanized = self.romanizer.convert(word)

        word = "பண்ணிட்டேன்"
        expected = "paṇṇiṭṭe:n"
        romanized = self.romanizer.convert(word)

        assert romanized == expected

        word = "உங்களுடைய"
        expected = "ungkaḷuṭaiya"
        romanized = self.romanizer.convert(word)

        assert romanized == expected

class TestTamilization(unittest.TestCase):
    def setUp(self):
        self.converter = Converter('romanization', 'tamil')
    
    def test_tamilization(self):
        word = "arisi"	
        expected = "அரிசி"

        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "aaDu"	
        expected = "ஆடு"
        tamil = self.converter.convert(word)
        assert tamil == expected	

        word = "ilai"	
        expected = "இலை"	
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "eeram"	
        expected = "ஈரம்"
        tamil = self.converter.convert(word)
        assert tamil == expected
        # rule ordering gives ஏரம்


        word = "uthaDu"	
        expected = "உதடு"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "udhaDu"	
        expected = "உதடு"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "oonjal"	
        expected = "ஊஞ்சல்"
        tamil = self.converter.convert(word)
        assert tamil == expected
        # ஓஞ்சல்

        word = "aivar"	
        expected = "ஐவர்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "oTTagam"	
        expected = "ஒட்டகம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "ODam"	
        expected = "ஓடம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "owvvai"	
        expected = "ஔவ்வை"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "auDadham"	
        expected = "ஔடதம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "kurangu"	
        expected = "குரங்கு"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "nya:nam"	
        expected = "ஞானம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "chandhramukhi"	
        expected = "சந்திரமுகி"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "oṭṭagam"	
        expected = "ஒட்டகம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "aNNam"	
        expected = "அண்ணம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "thamizh"	
        expected = "தமிழ்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "pazham"	
        expected = "பழம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "balam"	
        expected = "பலம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "yAr"	
        expected = "யார்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "ka:ttru"	
        expected = "காற்று"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "paLLi"	
        expected = "பள்ளி"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "vAram"	
        expected = "வாரம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "manam"	
        expected = "மனம்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "mahan"	
        expected = "மகன்"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "jeeraam"	
        expected = "ஜீராம்"
        tamil = self.converter.convert(word)
        assert tamil == expected 

        word = "shankha"	
        expected = "ஷன்க"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "hai"	
        expected = "ஹை"
        tamil = self.converter.convert(word)
        assert tamil == expected

        word = "thanḍam"	
        expected = "தண்டம்"
        tamil = self.converter.convert(word)
        assert tamil == expected
