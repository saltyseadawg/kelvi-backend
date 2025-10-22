from app.morphology import affixes


def test_get_prefix():
    sample_string = "abc123def"
    prefix = affixes.get_prefix(sample_string, "123")
    expected = "abc"
    assert prefix == expected


def test_get_prefix_none():
    sample_string = "abc123def"
    prefix = affixes.get_prefix(sample_string, "a")
    expected = None
    assert prefix == expected

    prefix = affixes.get_prefix(sample_string, ":)")
    assert prefix == expected


def test_get_suffix():
    sample_string = "abc123def"
    suffix = affixes.get_suffix(sample_string, "123")
    expected = "def"
    assert suffix == expected


def test_get_suffix_none():
    sample_string = "abc123def"
    suffix = affixes.get_suffix(sample_string, "def")
    expected = None
    assert suffix == expected

    suffix = affixes.get_suffix(sample_string, ":)")
    assert suffix == expected
