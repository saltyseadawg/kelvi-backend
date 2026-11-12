import re

from app.models import TamilForm, InputWord

from app.morphology import analyzer


def process_input_word(
    word_data: InputWord, tamilizer, romanizer, stanza_pipeline, tamil_dicts, glosser
):
    stanza_lemma = ""  # for testing
    gramble_lemma = ""  # for testing
    add_back_lemma = ""  # for testing
    first_word = word_data.user_input.split()[0]
    # unable to handle any hybrid Tamil + romanization words
    if re.search("[a-zA-Z]", word_data.user_input):
        tamil = tamilizer.convert(first_word)
        tamil = re.sub("[a-zA-Z]", "", tamil)
        roman = romanizer.convert(tamil)
        word_data.processed_input = TamilForm(tamil=tamil, romanization=roman)
    else:
        word_data.processed_input = TamilForm(
            tamil=first_word, romanization=romanizer.convert(first_word)
        )

    # try lemmatizer
    lemma, suffixal_material = analyzer.analyze_word_stanza(
        word_data.processed_input.tamil, pipeline=stanza_pipeline
    )
    defns = []
    tamil_dicts = tamil_dicts
    for d in tamil_dicts.values():
        defns.extend(d.search_word(lemma))
        stanza_lemma = lemma  # for testing
        if defns:
            lemmatization_method = "stanza"  # for testing
    if not defns:
        # try using gramble to find suffix

        # lemma, suffixal_material = analyzer.analyze_word_gramble(lemma, glosser)
        # --> this was the cause of the problem, bc "lemma" was drawing on the "lemma" stanza tried and failed to
        # find in line 34 instead of trying again with the actual input word
        
        lemma, suffixal_material = analyzer.analyze_word_gramble(
            word_data.processed_input.tamil, glosser
        )
        gramble_lemma = lemma  # for testing
        for d in tamil_dicts.values():
            defns.extend(d.search_word(lemma))
            if defns:
                lemmatization_method = "gramble_basic"  # for testing
    if not defns:
        # try add back to find lemma
        lemma = analyzer.analyze_word_add_back(lemma, suffixal_material, glosser)
        add_back_lemma = lemma  # for testing
        for d in tamil_dicts.values():
            defns.extend(d.search_word(lemma))
            lemmatization_method = "add_back"  # for testing
    if not defns:
        print(
            "lemma: " + lemma + " not found in dictionary"
        )  # for testing purposes, needs refactoring
        # raise HTTPException(status_code=404, detail="Word not found")
    word_data.root_definition = defns
    word_data.root = TamilForm(tamil=lemma, romanization=romanizer.convert(lemma))
    if suffixal_material:
        suffixal_material.romanization = romanizer.convert(suffixal_material.display)
        word_data.suffixal_material = suffixal_material

    lemma_data = [stanza_lemma, gramble_lemma, add_back_lemma, lemmatization_method]

    return word_data, lemma_data
