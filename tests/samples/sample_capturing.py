import logging
import sys

import pytest


def test_stdout():
    print("STDOUT")


def test_stderr():
    sys.stderr.write("STDERR")


def test_log():
    logging.debug("A debug statement")
    logging.info("An info statement")
