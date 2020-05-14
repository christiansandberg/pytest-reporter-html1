import pytest


count = 0


@pytest.mark.flaky(reruns=2)
def test_rerun():
    global count

    count += 1
    print("Rerun #%d" % count)
    assert False
