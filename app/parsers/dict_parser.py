import re
import json
from collections import OrderedDict

def new_entry():
    return {
        "variants": [],
        "romanized": [],
        "english": [],
        "subentries": OrderedDict(),
        "_variants_set": set(),
        "_roman_set": set()
    }

def add_unique(entry, key, value):
    set_key = "_variants_set" if key == "variants" else "_roman_set" if key == "romanized" else None
    if not value:
        return
    if set_key:
        if value not in entry[set_key]:
            entry[key].append(value)
            entry[set_key].add(value)
    else:
        if value not in entry[key]:
            entry[key].append(value)

def cleanup_entry(entry):
    entry.pop("_variants_set", None)
    entry.pop("_roman_set", None)
    for sub in entry["subentries"].values():
        cleanup_entry(sub)

def parse_tamil_dictionary(text):
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    dictionary = OrderedDict()

    current_headword = None
    current_entry = None
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]+')
    roman_pattern = re.compile(r'^[a-zA-Z()=]+$')
    dict_source = None
    for line in lines:
        if re.match(r'^[\u0B80-\u0BFF]+$', line):
            current_headword = line
            if current_headword not in dictionary:
                dictionary[current_headword] = new_entry()
            current_entry = dictionary[current_headword]
            add_unique(current_entry, "variants", line)
            continue

        words = line.split()
        last_target = current_entry
        english_buffer = []

        for word in words:
            if tamil_pattern.fullmatch(word):
                if word != current_headword:
                    if word not in current_entry["subentries"]:
                        current_entry["subentries"][word] = new_entry()
                    last_target = current_entry["subentries"][word]
                add_unique(last_target, "variants", word)

            elif roman_pattern.match(word):
                add_unique(last_target, "romanized", word)

            else:
                english_buffer.append(word)

        if english_buffer:
            add_unique(last_target, "english", " ".join(english_buffer))

    for entry in dictionary.values():
        cleanup_entry(entry)

    return dictionary


# ✅ Guess part of speech from English definitions
def guess_pos(definitions):
    text = " ".join(definitions).lower()
    if any(w in text for w in [" to ", " verb", "action"]):
        return "verb"
    if any(w in text for w in ["noun", "thing", "person", "place"]):
        return "noun"
    if any(w in text for w in ["adjective", "describing", "quality"]):
        return "adjective"
    return None


# ✅ Merge duplicates and convert to target schema
def convert_to_custom_schema(parsed_dict, source="custom.parsed"):
    merged = OrderedDict()

    # Merge duplicates by headword
    for headword, data in parsed_dict.items():
        if headword not in merged:
            merged[headword] = data
        else:
            # merge variants, romanizations, english
            for v in data["variants"]:
                add_unique(merged[headword], "variants", v)
            for r in data["romanized"]:
                add_unique(merged[headword], "romanized", r)
            for e in data["english"]:
                add_unique(merged[headword], "english", e)
            # merge subentries
            for sub_tamil, sub_data in data["subentries"].items():
                if sub_tamil not in merged[headword]["subentries"]:
                    merged[headword]["subentries"][sub_tamil] = sub_data
                else:
                    # merge inside existing subentry
                    for rv in sub_data["romanized"]:
                        add_unique(merged[headword]["subentries"][sub_tamil], "romanized", rv)
                    for ev in sub_data["english"]:
                        add_unique(merged[headword]["subentries"][sub_tamil], "english", ev)

    # Build final schema
    result = []
    entry_id = 1

    for headword, data in merged.items():
        romanization = data["romanized"][0] if data["romanized"] else None
        pos = guess_pos(data["english"])

        subentries = list(data["subentries"].items())
        centamil_equiv = None
        related_forms = []

        if subentries:
            first_tamil, first_sub = subentries[0]
            #TODO: include tamil equivs
            centamil_equiv = {
                "tamil": "",
                "romanization": ""
            }
            # Add ALL subentries (including first one) to related_forms
            for tamil, sub in subentries:
                related_forms.append({
                    "tamil": tamil,
                    "romanization": sub["romanized"][0] if sub["romanized"] else None
                })

        result.append({
            "id": entry_id,
            "lang": "Tamil",
            "dialect": None,
            "pos": pos,
            "romanization": romanization,
            "definitions": data["english"],
            "centamil_koduntamil_equiv": centamil_equiv,
            "related_forms": related_forms,
            "examples": None,
            "source": source
        })
        entry_id += 1

    return result

# remove the header line before running this cmd
def mcalpin_to_json(input_file: str, output_file: str):
    schema_mapped = {}
    with open(input_file, "r") as raw_data:
        data = raw_data.read()
        parsed = parse_tamil_dictionary(data)
        schema_mapped = convert_to_custom_schema(parsed, source="mcalpin")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema_mapped, f, ensure_ascii=False, indent=2)

    print(f"✅ mcalpin dictionary output to: {output_file}")