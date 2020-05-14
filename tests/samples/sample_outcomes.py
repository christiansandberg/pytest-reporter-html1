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


@pytest.mark.skip
def test_skipped():
    assert False


@pytest.mark.flaky(reruns=1)
def test_rerun():
    assert False
