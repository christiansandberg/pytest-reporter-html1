import re

import pytest
from bs4 import BeautifulSoup


pytest_plugins = ["pytester"]


@pytest.mark.parametrize(
    "args",
    [
        ("report.html", "--log-level=DEBUG"),
        ("split_report.html", "--split-report"),
        ("xdist_report.html", "-n", "4"),
    ],
    ids=lambda x: x[0],
)
def test_sample_report(args, testdir, pytestconfig):
    testdir.makeini([
        "[pytest]",
        "python_files=sample_*.py",
        "markers =",
        "   static_mark",
        "   dynamic_mark",
        "   mark_with_args",
    ])
    testdir.copy_example("samples")
    testdir.copy_example("../screenshot.png")

    report = "{}/report/{}".format(pytestconfig.rootdir, args[0])
    result = testdir.runpytest(
        *args[1:],
        "--template=html1/index.html",
        "--report=" + report
    )
    assert result.ret == 1
    with open(report) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    sample_outcomes = soup.find(
        string=re.compile(r"sample_outcomes\.py")
    ).find_parent("details")
    counts = sample_outcomes.find_all(class_="count")
    # failed, passed, error, xfailed, xpassed, skipped
    assert len(counts) == 6
    # 1 test of each
    for count in counts:
        assert count.string == "1"
