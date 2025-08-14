"""Used ChatGPT to help write this file."""

from app.models import TamilDictEntry, TamilForm

import re
import json


def parse_mcalpin(text):
    lines = [line for line in text.strip().split("\n") if line.strip()]
    tamil_dict = {}
    current_headword = None
    # some headwords words have () [], which i assume indicates variation
    headword_pattern = re.compile(r"^[^a-zA-Z]*$")
    tamil_pattern = re.compile(r"[\u0B80-\u0BFF]+")
    definition_pattern = re.compile(r"[^\u0B80-\u0BFF\s]+[a-zA-Z()=\s\W]+$")
    counter = 0
    for line in lines:
        try:
            if headword_pattern.match(line):
                current_headword = line.strip()
            if current_headword not in tamil_dict:
                tamil_dict[current_headword] = None
                continue
            related_forms = tamil_pattern.findall(line)[1:]
            tamil_forms = [TamilForm(tamil=form.strip()) for form in related_forms]

            definition = definition_pattern.search(line)[0].strip()
            entry = TamilDictEntry(
                definitions=[definition],
                related_forms=tamil_forms,
            )
            tamil_dict[current_headword] = entry
        except Exception:
            print(current_headword)
            tamil_dict.pop(current_headword)
            counter += 1

    print(f"Failed to parse: {counter}")
    return tamil_dict


# remove the header line before running this cmd
def mcalpin_to_json(input_file: str, output_file: str):
    with open(input_file, "r") as raw_data:
        data = raw_data.read()
        parsed = parse_mcalpin(data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed, f, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
    print(f"✅ mcalpin dictionary output to: {output_file}")


def parse_wiktionary_line(line: str) -> tuple[str, TamilDictEntry]:
    """Parses one JSON line from the Wiktionary-style Tamil dump."""
    data = json.loads(line)

    tamil_word = data.get("word")

    definitions = []
    for sense in data.get("senses", []):
        glosses = sense.get("glosses", [])
        definitions.extend(glosses)

    related_forms = None
    if "related" in data:
        related_forms = [
            TamilForm(tamil=rf["word"]) for rf in data["related"] if "word" in rf
        ]

    entry = TamilDictEntry(
        pos=data.get("pos"),
        definitions=definitions,
        related_forms=related_forms,
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
            if tamil_word:
                # Store as {word: {... entry data ...}}
                data[tamil_word] = entry
        outfile.write(
            json.dumps(data, default=lambda o: o.__dict__, indent=4, ensure_ascii=False)
        )
