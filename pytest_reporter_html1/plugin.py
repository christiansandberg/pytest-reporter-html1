from pathlib import Path
from datetime import datetime, timedelta
import re
from inspect import cleandoc
from base64 import b64encode
import shutil
import mimetypes

from jinja2 import Environment, FileSystemLoader, select_autoescape, evalcontextfilter, Markup
from ansi2html import Ansi2HTMLConverter
from ansi2html.style import get_styles
from docutils.core import publish_parts
import htmlmin


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
        help="store CSS and image files under 'assets' directory.",
    )


def pytest_configure(config):
    config.pluginmanager.register(TemplatePlugin(config))


class TemplatePlugin:

    def __init__(self, config):
        self.self_contained = not config.getoption("--split-report")
        self._css = None
        self._assets = []

    def pytest_reporter_loader(self, dirs, config):
        conv = Ansi2HTMLConverter(escaped=False)
        self.env = env = Environment(
            loader=FileSystemLoader(dirs + [str(TEMPLATE_PATH)]),
            autoescape=select_autoescape(["html", "htm", "xml"]),
        )
        env.globals["get_ansi_styles"] = get_styles
        env.globals["self_contained"] = self.self_contained
        env.filters["css"] = self._cssfilter
        env.filters["asset"] = self._assetfilter
        env.filters["repr"] = repr
        env.filters["strftime"] = lambda ts, fmt: datetime.fromtimestamp(ts).strftime(fmt)
        env.filters["timedelta"] = lambda ts: timedelta(seconds=ts)
        env.filters["ansi"] = lambda s: conv.convert(s, full=False)
        env.filters["cleandoc"] = cleandoc
        env.filters["rst"] = lambda s: publish_parts(source=s, writer_name="html5")["body"]
        env.filters["css_minify"] = lambda s: re.sub(r"\s+", " ", s)
        return env

    def pytest_reporter_context(self, context, config):
        context.setdefault("colors", COLORS)

    def _cssfilter(self, css):
        if self.self_contained:
            return Markup("<style>") + css + Markup("</style>")
        else:
            self._css = css
            return Markup('<link rel="stylesheet" type="text/css" href="html1.css">')

    def _assetfilter(self, src):
        path = TEMPLATE_PATH / src
        if self.self_contained:
            mimetype, _ = mimetypes.guess_type(src)
            content = path.read_bytes()
            return (
                "data:" + mimetype + ";base64," + b64encode(content).decode("utf-8")
            )
        else:
            self._assets.append(path)
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
