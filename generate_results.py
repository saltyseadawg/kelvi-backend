import csv

from app.models import InputWord

from app.morphology import stanza_utils
from app.routers import e2e_testing

from app.morphology.glosser.Glosser import Glosser
from app.data.dictionaries.WordDict import WordDict


from app.lang_mappings.converter import Converter, Romanizer


import stanza


def get_results(file: str):
    # initialize all the stuffs
    romanizer = Romanizer("tamil", "romanization")
    tamilizer = Converter("romanization", "tamil")
    stanza_pipeline = stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        # uncomment for local development
        # download_method="reuse_resources"
        download_method=None,
    )
    glosser = Glosser()
    tamil_dicts = {}
    dict_names = ["mcalpin", "wiktionary"]
    for name in dict_names:
        tamil_dicts[name] = WordDict(name)
    tamil_dicts = tamil_dicts

    # process the test data words
    words_info = []
    with open(file, newline="") as csvfile:
        input_file = csv.reader(csvfile)
        for token in input_file:
            test_word = InputWord(user_input=token[0])
            processed_word_data = {}
            processed_word_data["test_word"] = token
            word_results = e2e_testing.process_input_word(
                word_data=test_word,
                tamilizer=tamilizer,
                romanizer=romanizer,
                stanza_pipeline=stanza_pipeline,
                tamil_dicts=tamil_dicts,
                glosser=glosser,
            )[0]
            lemma_data = e2e_testing.process_input_word(
                word_data=test_word,
                tamilizer=tamilizer,
                romanizer=romanizer,
                stanza_pipeline=stanza_pipeline,
                tamil_dicts=tamil_dicts,
                glosser=glosser,
            )[1]
            processed_word_data["user_input"] = word_results.user_input
            processed_word_data["tamil_root"] = word_results.root.tamil
            processed_word_data["rom_root"] = word_results.root.romanization
            processed_word_data["prefix"] = word_results.prefixal_material
            processed_word_data["suffix"] = word_results.suffixal_material
            processed_word_data["definitions"] = word_results.root_definition
            processed_word_data["stanza_lemma"] = lemma_data[0]
            processed_word_data["gramble_lemma"] = lemma_data[1]
            processed_word_data["add_back_lemma"] = lemma_data[2]
            processed_word_data["lemmatization_method"] = lemma_data[3]
            words_info.append(processed_word_data)

    # write the results into an output file
    with open("kelvi_results.csv", "w", newline="") as csvfile:
        fieldnames = [
            "test_word",
            "user_input",
            "stanza_lemma",
            "gramble_lemma",
            "add_back_lemma",
            "lemmatization_method",
            "tamil_root",
            "rom_root",
            "prefix",
            "suffix",
            "definitions",
        ]
        output_file = csv.DictWriter(csvfile, fieldnames=fieldnames)
        output_file.writeheader()
        output_file.writerows(words_info)
    return output_file


def stanza_test(word: str):
    pipeline = stanza.Pipeline(
        lang="ta",
        processors="tokenize,mwt,pos,lemma",
        download_method="reuse_resources",
    )
    stanza_result = stanza_utils.process_word(pipeline, word)
    lemma = stanza_result.lemma
    return lemma
