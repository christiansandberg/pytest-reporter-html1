import pytest


@pytest.fixture
def broken():
    raise RuntimeError("Something went wrong")


def test_failed():
    assert False


def test_passed():
    assert True


def test_error(broken):
    assert True


@pytest.mark.xfail(reason="Always asserts False")
def test_xfailed():
    assert False


@pytest.mark.xfail
def test_xpassed():
    assert True


@pytest.mark.skip
def test_skipped():
    assert False
