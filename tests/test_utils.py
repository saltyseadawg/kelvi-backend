from app.parsers import utils


def test_remove_trailing_brackets():
    word = "அம்மா (ammā)"
    result = utils.remove_trailing_brackets(word)
    expected = "அம்மா"
    assert result == expected

    word = "அம்மா (1234) (ammā)"
    result = utils.remove_trailing_brackets(word)
    expected = "அம்மா"
    assert result == expected
