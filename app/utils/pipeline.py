def get_first_word_from_pipeline(doc) -> dict:
    for s in doc.sentences:
        for w in s.words:
            return w