from app.models import TamilDictEntry, TamilForm

import re
import json

# use GNU split command to so split raw wikiextract data into smaller files 

def parse_wiktionary_line(line: str) -> tuple[str, TamilDictEntry]:
    """Parses one JSON line from the Wiktionary-style Tamil dump."""
    data = json.loads(line)

    tamil_word = data.get("word")

    definitions = []
    for sense in data.get("senses", []):
        glosses = sense.get("glosses", [])
        definitions.extend(glosses)
    
    related_forms = {}
    try:
        for synonym in data.get('synonyms', []):
            if synonym:
                word = synonym.get("word")
                related_entry = TamilDictEntry(
                    definitions = [].extend(data.get('glosses', []))
                )
                related_forms[word] = related_entry
    except Exception:
        print(tamil_word)


    entry = TamilDictEntry(
        pos=data.get("pos"),
        definitions=definitions,
        related_forms=None,
        source="wiktionary",
    )

    return tamil_word, entry, related_forms


def reformat_wiktionary(input_path: str, output_path: str):
    """Reads the raw JSONL dictionary and writes a reformatted JSONL file."""
    data = []
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            line = line.strip()
            if not line:
                continue

            tamil_word, entry, related_words = parse_wiktionary_line(line)
            if tamil_word:
                # Store as {word: {... entry data ...}}
                data[tamil_word] = entry
                print(tamil_word)
                # add related words as headwords to be searchable
                for key, value in related_words:
                    if key in data:
                        data[key].definitions.extend(value)
                    else:
                        data[key] = value
        outfile.write(
            json.dumps(data, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
        )

def extract_entries(input_path: str, output_path: str, lang: str):
    """Reads the raw JSONL dictionary and writes a reformatted JSONL file."""
    with (
        open(input_path, "r", encoding="utf-8") as infile,
        open(output_path, "w", encoding="utf-8") as outfile,
    ):
        entries = []
        for line in infile:
            line = line.strip()
            line_data = json.loads(line)
            if line_data.get('lang', None) == lang:
                entries.append(line + '\n')
        outfile.writelines(entries)

