import logging
import sys
import pytest


@pytest.fixture
def print_example():
    print("Print from setup")
    yield
    print("Print from teardown")


def test_stdout(print_example):
    print("\n".join("asd" * 40 for _ in range(100)))


def test_stderr():
    sys.stderr.write("STDERR")


def test_log():
    logging.debug("A debug statement")
    logging.info("An info statement")
