from datetime import datetime, timedelta
import re
from functools import partial
import os.path
from pathlib import Path
from inspect import cleandoc
from base64 import b64encode

import pytest

try:
    from ansi2html import Ansi2HTMLConverter
    from ansi2html.style import get_styles
except ImportError:
    HAS_ANSI = False
else:
    HAS_ANSI = True
    conv = Ansi2HTMLConverter(escaped=False)

try:
    from docutils.core import publish_parts
except ImportError:
    publish_parts = None

try:
    import htmlmin
except ImportError:
    htmlmin = None


def pytest_reporter_template_dir():
    return os.path.join(os.path.dirname(__file__), "templates")


def rst2html(rst):
    if publish_parts is not None:
        parts = publish_parts(source=rst, writer_name="html5")
        return parts["body"]
    else:
        return re.sub(r"\n", "<br>", rst)


@pytest.hookimpl(tryfirst=True)
def pytest_reporter_modify_env(env):
    env.filters["repr"] = repr
    env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
    env.filters["timedelta"] = lambda ts: timedelta(seconds=ts)
    env.filters["ansi"] = partial(conv.convert, full=False) if HAS_ANSI else str
    env.filters["cleandoc"] = cleandoc
    env.filters["rst2html"] = rst2html
    env.filters["base64"] = lambda s: b64encode(b).decode("utf-8")
    env.filters["css_minify"] = partial(re.sub, r"\s+", " ")


def pytest_reporter_context(context):
    if HAS_ANSI:
        context["get_ansi_styles"] = get_styles
    icons = Path(__file__).parent / "templates" / "html1" / "icons"
    context["icons"] = {
        icon.stem: "data:image/svg+xml;base64," + b64encode(icon.read_bytes()).decode("utf-8") for icon in icons.glob("*.svg")
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_reporter_render():
    outcome = yield
    html = outcome.get_result()
    if htmlmin is not None:
        minified = htmlmin.minify(html, remove_comments=True)
        outcome.force_result(minified)
