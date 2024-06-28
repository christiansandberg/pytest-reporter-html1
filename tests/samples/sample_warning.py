from warnings import warn


def test_warning():
    warn("This is a user warning.", UserWarning)
    warn("This is a deprecation.", DeprecationWarning)
