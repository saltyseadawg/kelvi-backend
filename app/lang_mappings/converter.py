import logging
import re

from g2p import make_g2p


class Converter:
    def __init__(self, in_lang: str, out_lang: str):
        self.transducer = make_g2p(in_lang, out_lang)

    def convert(self, input: str):
        try:
            return self.transducer(input).output_string
        except Exception:
            logging.error(f"Failed to convert: {input}")




class Romanizer(Converter):
    NO_TAMIL_RE = re.compile(r'^[^\u0B80-\u0BFF]*$')

    def convert(self, input: str):
        roman = self.transducer(input).output_string
        if not bool(self.NO_TAMIL_RE.match(roman)):
            roman = ''
            logging.error(f"Failed to romanize: {input}")
        return roman 
