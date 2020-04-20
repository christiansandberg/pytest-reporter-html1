from datetime import datetime
import re
from functools import partial
import os.path

import pytest
try:
    from ansi2html import Ansi2HTMLConverter, style
    conv = Ansi2HTMLConverter(escaped=False)
except ImportError:
    conv = None
    style = None


def ansi(content):
    if conv is not None:
        return conv.convert(content, full=False)
    else:
        return content


def get_styles(*args, **kwargs):
    if style is not None:
        return style.get_styles(*args, **kwargs)
    else:
        return ""


def pytest_reporter_template_dir():
    return os.path.join(os.path.dirname(__file__), "templates")


@pytest.hookimpl(tryfirst=True)
def pytest_reporter_modify_env(env):
    env.add_extension("jinja2.ext.debug")
    env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
    env.filters["ansi"] = ansi
    env.filters["css_minify"] = partial(re.sub, r"\s+", " ")
    env.filters["html_minify"] = partial(re.sub, r">\s+<", "> <")


def pytest_reporter_context():
    return {"ansi_get_styles": get_styles}
