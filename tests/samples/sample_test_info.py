import pytest


@pytest.mark.parametrize("i", range(3))
def test_parametrized(i):
    assert i < 2


@pytest.mark.mark1
@pytest.mark.mark_with_args("positional", keyword=1234)
def test_markers():
    pass


def test_with_documentation():
    """This is a documentation.

    Header 1
    --------

    This is a link to `pytest`_.

    Here is a list:

    1. One
    2. Two
    3. Three

    .. _`pytest`: https://github.com/pytest-dev/pytest
    """
    pass


def test_user_properties(record_property):
    record_property("string", "Some string value")
    record_property("integer", 123)
    record_property("xml", "<blink>Blink!</blink>")
    record_property("url", "https://github.com/christiansandberg/pytest-reporter-html1")
