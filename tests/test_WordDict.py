import json
import pytest
from unittest.mock import mock_open, patch

# Import your class and dependencies
from app.data.dictionaries.WordDict import WordDict
from app.models import InputWord, TamilForm, TamilDictEntry


@pytest.fixture
def sample_dict_data():
    return {
        "அகராதி": {
            "pos": None,
            "definitions": ["dictionary"],
            "examples": None,
            "source": None,
            "romanization": None,
            "centamil_koduntamil_equiv": None,
            "related_forms": [{"tamil": "டிக்ஷனரி", "romanization": None}],
        }
    }


def test_search_word_found(sample_dict_data):
    mock_file_content = json.dumps(sample_dict_data)

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("json.load", return_value=sample_dict_data):
            wd = WordDict(dict_filepath="test_dict")
            result = wd.search_word("அகராதி")

    assert isinstance(result, InputWord)
    assert result.user_input == "அகராதி"
    assert isinstance(result.root, TamilForm)
    assert isinstance(result.root_definition, TamilDictEntry)
    assert result.root_definition.definitions == ["dictionary"]


def test_search_word_not_found(sample_dict_data):
    mock_file_content = json.dumps(sample_dict_data)

    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("json.load", return_value=sample_dict_data):
            wd = WordDict(dict_filepath="test_dict")
            result = wd.search_word("புத்தகம்")

    assert result is None


def test_init_loads_correct_file():
    with patch("builtins.open", mock_open(read_data="{}")) as mock_file:
        with patch("json.load", return_value={}):
            WordDict(dict_filepath="custom_dict")

    mock_file.assert_called_once_with(
        "app/data/dictionaries/custom_dict.json", "r", encoding="utf-8"
    )
