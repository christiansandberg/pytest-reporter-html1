import mimetypes
import re
import shutil
from base64 import b64encode
from datetime import datetime, timedelta
from inspect import cleandoc
from pathlib import Path
import warnings

import htmlmin
from ansi2html import Ansi2HTMLConverter
from ansi2html.style import get_styles
from docutils.core import publish_parts
from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateNotFound,
    Markup,
    select_autoescape,
)

from . import __version__

TEMPLATE_PATH = Path(__file__).parent / "templates"
# category/style: background-color, color
COLORS = {
    "passed": ("#43A047", "#FFFFFF"),
    "failed": ("#F44336", "#FFFFFF"),
    "error": ("#B71C1C", "#FFFFFF"),
    "xfailed": ("#EF9A9A", "#333333"),
    "xpassed": ("#A5D6A7", "#333333"),
    "skipped": ("#9E9E9E", "#FFFFFF"),
    "rerun": ("#FBC02D", "#333333"),
    "warning": ("#FBC02D", "#333333"),
    "green": ("#43A047", "#FFFFFF"),
    "red": ("#E53935", "#FFFFFF"),
    "yellow": ("#FBC02D", "#333333"),
}


def pytest_addoption(parser):
    group = parser.getgroup("report generation")
    group.addoption(
        "--split-report",
        action="store_true",
        help="store CSS and image files separately from the HTML.",
    )


def pytest_configure(config):
    config.pluginmanager.register(TemplatePlugin(config))


def css_minify(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"/\*.*?\*/", "", s)
    return s


class TemplatePlugin:
    def __init__(self, config):
        self.self_contained = not config.getoption("--split-report")
        self._css = None
        self._assets = []
        self._dirs = []

    def pytest_reporter_loader(self, dirs, config):
        self._dirs = dirs + [str(TEMPLATE_PATH)]
        conv = Ansi2HTMLConverter(escaped=False)
        self.env = env = Environment(
            loader=FileSystemLoader(self._dirs),
            autoescape=select_autoescape(["html", "htm", "xml"]),
        )
        env.globals["get_ansi_styles"] = get_styles
        env.globals["self_contained"] = self.self_contained
        env.globals["__version__"] = __version__
        env.filters["css"] = self._cssfilter
        env.filters["asset"] = self._assetfilter
        env.filters["repr"] = repr
        env.filters["id"] = id
        env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
        env.filters["timedelta"] = lambda ts: timedelta(seconds=ts)
        env.filters["ansi"] = lambda s: conv.convert(s, full=False)
        env.filters["cleandoc"] = cleandoc
        env.filters["rst"] = lambda s: publish_parts(source=s, writer_name="html5")["body"]
        env.filters["css_minify"] = css_minify
        return env

    def pytest_reporter_context(self, context, config):
        context.setdefault("colors", COLORS)
        context.setdefault("time_format", "%Y-%m-%d %H:%M:%S")

    def _cssfilter(self, css):
        if self.self_contained:
            return Markup("<style>") + css + Markup("</style>")
        else:
            self._css = css
            return Markup('<link rel="stylesheet" type="text/css" href="html1.css">')

    def _assetfilter(self, src):
        path = None
        for parent in [".", *self._dirs]:
            maybe_file = Path(parent) / src
            if maybe_file.is_file():
                path = maybe_file
                break
        if not path:
            warnings.warn("Could not find file '%s'" % src)
            path = src

        if self.self_contained:
            mimetype, _ = mimetypes.guess_type(src)
            content = path.read_bytes()
            return "data:" + mimetype + ";base64," + b64encode(content).decode("utf-8")
        else:
            self._assets.append(path)
            # Put all assets in the same directory as the HTML and CSS
            return path.name

    def pytest_reporter_render(self, template_name, dirs, context):
        try:
            template = self.env.get_template(template_name)
        except TemplateNotFound:
            return
        html = template.render(context)
        minified = htmlmin.minify(html, remove_comments=True)
        return minified

    def pytest_reporter_finish(self, path, context, config):
        assets = path.parent
        # assets.mkdir(parents=True, exist_ok=True)
        if self._css:
            style_css = assets / "html1.css"
            style_css.write_text(self._css)
        for asset in self._assets:
            shutil.copy(asset, assets)
