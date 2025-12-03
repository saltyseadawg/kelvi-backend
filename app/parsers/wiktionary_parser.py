from app.models import TamilDictEntry
from app.parsers import utils

import json

# use GNU split command to so split raw wikiextract data into smaller files


def parse_wiktionary_line(line: str) -> tuple[str, TamilDictEntry]:
    """Parses one JSON line from the Wiktionary-style Tamil dump."""
    data = json.loads(line)

    tamil_word = utils.remove_trailing_brackets(data.get("word")).strip()
    definitions = []
    for sense in data.get("senses", []):
        glosses = sense.get("glosses", [])
        definitions.extend(glosses)

    entry = TamilDictEntry(
        pos=data.get("pos"),
        definitions=definitions,
        related_forms=None,
        source="wiktionary",
    )

    return tamil_word, entry


def reformat_wiktionary(input_path: str, output_path: str):
    """Reads the raw JSONL dictionary and writes a reformatted JSONL file."""
    data = {}
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            line = line.strip()
            if not line:
                continue

            tamil_word, entry = parse_wiktionary_line(line)
            if tamil_word in data:
                data[tamil_word].definitions.extend(entry.definitions)
            else:
                # Store as {word: {... entry data ...}}
                data[tamil_word] = entry
        outfile.write(
            json.dumps(data, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
        )


def extract_entries(input_path: str, output_path: str, lang: str):
    """Extract the entries from the raw Wikiextract file of the target language."""
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        entries = []
        for line in infile:
            line = line.strip()
            line_data = json.loads(line)
            if line_data.get("lang", None) == lang:
                entries.append(line + "\n")
        outfile.writelines(entries)


def parse_related_words(line: str):
    data = json.loads(line)
    word = utils.remove_trailing_brackets(data.get("word")).strip()
    related = {}
    synonyms = data.get("synonyms", None)
    if synonyms:
        for s in synonyms:
            related_word = utils.remove_trailing_brackets(s.get("word")).strip()
            related[related_word] = None
    for sense in data.get("senses"):
        synonyms = sense.get("synonyms", [])
        definition = sense.get("glosses", None)
        for s in synonyms:
            related_word = utils.remove_trailing_brackets(s.get("word")).strip()
            related[related_word] = definition

    return word, related


def add_related_words(raw_data_path: str, modified_data_path: str, output_file: str):
    data = {}
    words_to_add = {}
    with open(modified_data_path) as modified_data:
        data = json.load(modified_data)
    with open(raw_data_path, "r", encoding="utf-8") as raw_file:
        for line in raw_file:
            line = line.strip()
            if not line:
                continue
            word, related = parse_related_words(line)
            for related_entry, definition in related.items():
                if related_entry in data:
                    continue
                if definition:
                    words_to_add[related_entry] = TamilDictEntry(
                        definitions=definition,
                        source="wiktionary",
                    )
                else:
                    words_to_add[related_entry] = TamilDictEntry(
                        definitions=data[word].get("definitions"),
                        source="wiktionary",
                    )
    data.update(words_to_add)
    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write(
            json.dumps(data, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
        )
