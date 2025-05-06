from base64 import b64encode

import pytest_html


SCREENSHOT_PATH = "screenshot.png"
with open(SCREENSHOT_PATH, "rb") as fp:
    SCREENSHOT_DATA = fp.read()


def test_with_extras(extras):
    extras.append(pytest_html.extras.image(SCREENSHOT_PATH, name="Local file"))
    extras.append(pytest_html.extras.png(SCREENSHOT_DATA, name="Raw file"))
    extras.append(pytest_html.extras.png(b64encode(SCREENSHOT_DATA).decode("utf-8"), name="Base64 file"))
    extras.append(pytest_html.extras.html("This is some <strong>HTML</strong>!"))
    extras.append(pytest_html.extras.text("<lorem ipsum> " * 100))
    extras.append(pytest_html.extras.url("http://www.example.com/"))
    extras.append(pytest_html.extras.json({"content": {"list": [1, 2, 3]}}))
