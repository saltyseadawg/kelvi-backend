def get_prefix(word: str, stem: str) -> str:
    prefix = word.split(stem)[0]
    if prefix in (word, ""):
        prefix = None
    return prefix


def get_suffix(word: str, stem: str) -> str:
    suffix = word.split(stem)
    if len(suffix) < 2:
        suffix = suffix[0]
    else:
        suffix = suffix[1]

    if suffix in (word, ""):
        suffix = None
    return suffix
