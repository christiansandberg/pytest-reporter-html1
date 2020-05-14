import pytest


@pytest.mark.parametrize("i", range(3))
def test_parametrized(i):
    assert i < 2


def test_with_documentation():
    """This is a documentation.

    Header 1
    --------

    This is a link to `pytest`_.

    .. _`pytest`: https://github.com/pytest-dev/pytest
    """
    pass
