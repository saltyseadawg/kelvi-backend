import logging

from g2p import make_g2p


class Converter:
    def __init__(self, in_lang: str, out_lang: str):
        self.transducer = make_g2p(in_lang, out_lang)

    def convert(self, input: str):
        try:
            return self.transducer(input).output_string
        except Exception:
            logging.error(f"Failed to convert: {input}")
