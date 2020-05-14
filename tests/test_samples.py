import pytest
import _pytest


pytest_plugins = ["pytester"]


def test_sample_report(testdir, pytestconfig):
    testdir.makeini("[pytest]\npython_files=sample_*.py\n")
    testdir.copy_example("sample_outcomes.py")
    testdir.copy_example("sample_capturing.py")
    testdir.copy_example("sample_test_info.py")

    report = "{}/report/report.html".format(pytestconfig.rootdir)
    testdir.runpytest(
        "--log-level=DEBUG",
        "--template=html1/index.html",
        "--report=" + report
    )
    with open(report) as fp:
        html = fp.read()

    assert "<html" in html
