import re

from app.models import TamilForm, InputWord

from app.morphology import analyzer


def process_input_word(word_data: InputWord, tamilizer, romanizer, stanza_pipeline, tamil_dicts, glosser):
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
    if not defns:
        # try using gramble to find suffix
        if lemma:
            print(lemma)
        if not lemma:
            print("lemma missing")
        else:
            lemma, suffixal_material = analyzer.analyze_word_gramble(
                lemma, glosser
            )
            for d in tamil_dicts.values():
                defns.extend(d.search_word(lemma))
    if not defns:
        # try add back to find lemma
        lemma = analyzer.analyze_word_add_back(
            lemma, suffixal_material, glosser
        )
        for d in tamil_dicts.values():
            defns.extend(d.search_word(lemma))
    if not defns:
        raise HTTPException(status_code=404, detail="Word not found")
    word_data.root_definition = defns
    word_data.root = TamilForm(
        tamil=lemma, romanization=romanizer.convert(lemma)
    )
    if suffixal_material:
        suffixal_material.romanization = romanizer.convert(
            suffixal_material.display
        )
        word_data.suffixal_material = suffixal_material

    return word_data


def get_results(input_file: str):
    #input_file should be csv file of test cases with [lemma etc] in that order but are only passing the input into the function
    #output_file = open(input_file, "a") # open file to append
    for line in input_file:
        print(line)
            #test_word = line.input #the first index/element in that line should be the input
            #word_results = e2e_testing.process_input_word(word_data=test_word, tamilizer=self.tamilizer, 
            #romanizer=self.romanizer, stanza_pipeline=self.stanza_pipeline, tamil_dicts=self.tamil_dicts, 
            #glosser=self.glosser)
            #write word_results.user_input to that line
            #write word_results.root.romanization
            #write word_results.root.tamil
            #write word_results.prefixal_material
            #write word_results.suffixal_material
    #return output_file


