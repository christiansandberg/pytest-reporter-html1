from pathlib import Path
from datetime import datetime, timedelta
import re
from inspect import cleandoc
from base64 import b64encode

from jinja2 import Environment, FileSystemLoader, select_autoescape
from ansi2html import Ansi2HTMLConverter
from ansi2html.style import get_styles
from docutils.core import publish_parts
import htmlmin


TEMPLATE_PATH = Path(__file__).parent / "templates"
ICONS_PATH = TEMPLATE_PATH / "html1" / "icons"


def pytest_reporter_context(context, config):
    # category/style: background-color, color
    context.setdefault("colors", {
        "passed": ("#43A047", "#FFFFFF"),
        "failed": ("#F44336", "#FFFFFF"),
        "error": ("#B71C1C", "#FFFFFF"),
        "xfailed": ("#EF9A9A", "#333333"),
        "xpassed": ("#A5D6A7", "#333333"),
        "skipped": ("#9E9E9E", "#FFFFFF"),
        "warning": ("#FBC02D", "#333333"),
        "green": ("#43A047", "#FFFFFF"),
        "red": ("#E53935", "#FFFFFF"),
        "yellow": ("#FBC02D", "#333333"),
    })

def pytest_reporter_render(template_name, dirs, context):
    conv = Ansi2HTMLConverter(escaped=False)
    env = Environment(
        loader=FileSystemLoader(dirs + [str(TEMPLATE_PATH)]),
        autoescape=select_autoescape(["html", "htm", "xml"]),
    )
    env.globals["icons"] = {
        icon.stem: (
            "data:image/svg+xml;base64," +
            b64encode(icon.read_bytes()).decode("utf-8")
        ) for icon in ICONS_PATH.glob("*.svg")
    }
    env.globals["get_ansi_styles"] = get_styles
    env.filters["repr"] = repr
    env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
    env.filters["timedelta"] = lambda ts: timedelta(seconds=ts)
    env.filters["ansi"] = lambda s: conv.convert(s, full=False)
    env.filters["cleandoc"] = cleandoc
    env.filters["rst"] = lambda s: publish_parts(source=s, writer_name="html5")["body"]
    env.filters["css_minify"] = lambda s: re.sub(r"\s+", " ", s)

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        return
    html = template.render(context)
    minified = htmlmin.minify(html, remove_comments=True)
    return minified
