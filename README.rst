=====================
pytest-reporter-html1
=====================

.. image:: https://img.shields.io/pypi/v/pytest-reporter-html1.svg
    :target: https://pypi.org/project/pytest-reporter-html1
    :alt: PyPI version

A basic HTML report for `pytest`_ using `Jinja2`_ template engine.
Based on `pytest-reporter`_ which provides the data to the template.


Features
--------

* Overview of files, tests, and phases with expandable sections
* Includes information about tests such as documentation, markers, and fixtures
* Fairly mobile friendly
* Complies with Jenkins default CSP policy (with ``--split-report``)
* Support for `pytest-metadata`_ and `pytest-rerunfailures`_
* May be used as a base template for customization

.. image:: https://raw.githubusercontent.com/christiansandberg/pytest-reporter-html1/master/screenshot.png
    :alt: Screenshot


Installation
------------

You can install "pytest-reporter-html1" via `pip`_ from `PyPI`_::

    $ pip install pytest-reporter-html1


Usage
-----

Specify the html1 template and the output path of the report::

    $ pytest --template=html1/index.html --report=report.html

By default the report is self-contained, but you can separate CSS, images,
and JavaScript by specifying the ``--split-report`` option.


Customization
-------------

You can inherit this template in your own to tailor parts of it to your own needs.
It defines various blocks which you can override using `template inheritance`_.

.. code:: html

    {% extends "html1/index.html" %}
    {% block style %}
        {{ super() }}
        header {
            background-color: black;
        }
    {% endblock %}

Some additional filters are available for templates to use:

``asset(path_or_content, extension)``
    Takes a path to a local file or a raw bytes object and either returns a
    base64 encoded URL or a new relative URL to a copy depending on if the
    report is self-contained or not.

    .. code:: html

        <img src="{{ 'path/to/image.png'|asset }}">
        <img src="{{ raw_byte_data|asset('png') }}">

``ansi(s)``
    Convert ANSI color codes to HTML.

``strftime(value, format)``
    Format a Unix timestamp using `datetime.strftime`_.

    .. code:: html

        Started: {{ started|strftime('%Y-%m-%d %H:%M:%S') }}

``timedelta(value)``
    Convert a time in seconds to a `timedelta`_ object.

``rst(s)``
    Convert reStructuredText to HTML.


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Jinja2`: https://jinja.palletsprojects.com/
.. _`template inheritance`: https://jinja.palletsprojects.com/en/master/templates/#template-inheritance
.. _`file an issue`: https://github.com/christiansandberg/pytest-reporter-html1/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pytest-reporter`: https://github.com/christiansandberg/pytest-reporter
.. _`pytest-metadata`: https://github.com/pytest-dev/pytest-metadata
.. _`pytest-rerunfailures`: https://github.com/pytest-dev/pytest-rerunfailures
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
.. _`datetime.strftime`: https://docs.python.org/3/library/datetime.html#datetime.datetime.strftime
.. _`timedelta`: https://docs.python.org/3/library/datetime.html#timedelta-objects
