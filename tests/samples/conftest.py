from base64 import b64encode
import pytest


SCREENSHOT_PATH = "screenshot.png"
with open(SCREENSHOT_PATH, "rb") as fp:
    SCREENSHOT_DATA = fp.read()


EXTRAS = [
    {
        "name": "Local file",
        "format": "image",
        "content": SCREENSHOT_PATH,
    },
    {
        "name": "Raw file",
        "format": "image",
        "content": SCREENSHOT_DATA,
        "extension": "png",
    },
    {
        "name": "Base64 file",
        "format": "image",
        "content": b64encode(SCREENSHOT_DATA).decode("utf-8"),
        "extension": "png",
    },
    {
        "name": "HTML",
        "format": "html",
        "content": "This is some <strong>HTML</strong>!",
    },
    {
        "name": "Text",
        "format": "text",
        "content": "<lorem ipsum> " * 100,
    },
    {
        "name": "URL",
        "format": "url",
        "content": "https://christiansandberg.com/",
    },
    {
        "name": "JSON",
        "format": "json",
        "content": {"content": {"list": [1, 2, 3]}},
    },
    {
        "name": "Unknown",
        "format": "unknown",
        "content": "???",
    },
]


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and item.name == 'test_with_extras':
        report.extra = EXTRAS
