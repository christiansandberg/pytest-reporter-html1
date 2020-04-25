from datetime import datetime, timedelta
import re
from functools import partial
import os.path

import pytest

try:
    from ansi2html import Ansi2HTMLConverter
    from ansi2html.style import get_styles
except ImportError:
    conv = None
    get_styles = None
else:
    conv = Ansi2HTMLConverter(escaped=False)


def pytest_reporter_template_dir():
    return os.path.join(os.path.dirname(__file__), "templates")


@pytest.hookimpl(tryfirst=True)
def pytest_reporter_modify_env(env):
    env.add_extension("jinja2.ext.debug")
    env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
    env.filters["timedelta"] = lambda ts: timedelta(seconds=ts)
    env.filters["ansi"] = partial(conv.convert, full=False) if conv else str
    env.filters["css_minify"] = partial(re.sub, r"\s+", " ")
    env.filters["html_minify"] = partial(re.sub, r">\s+<", "> <")


def pytest_reporter_context(context):
    context["ansi_get_styles"] = get_styles
