LOGGING EXTRAS
===============

A collection of various python logging extensions.

[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blueviolet?logo=python&logoColor=green)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-blue?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![PyPi Publish](https://github.com/zobayer1/logging-extras/actions/workflows/python-publish.yml/badge.svg)
[![Build Status](https://travis-ci.com/zobayer1/logging-extras.svg?branch=main)](https://travis-ci.com/zobayer1/logging-extras)
[![Documentation Status](https://readthedocs.org/projects/logging-extras/badge/?version=latest)](https://logging-extras.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-ff69b4.svg)](https://github.com/zobayer1/logging-extras/blob/main/LICENSE)

Documentation
-------------
[https://logging-extras.readthedocs.io/en/latest/](https://logging-extras.readthedocs.io/en/latest/)

Distribution
------------

To create a source and wheel distribution, run:

    python -m pip install wheel
    python setup.py clean sdist bdist_wheel

It is recommended to use a virtualenv.

Installation
------------

Download the latest binary or source package from github [logging-extras releases](https://github.com/zobayer1/logging-extras/releases)

Install wheel package with `pip`:

    pip install logging_extras-{tags}.whl

Install source package as editable:

    tar -xf logging-extras-{tags}.tar.gz
    cd logging-extras-{tags}
    pip install -e .

Please refer to documentation pages for available modules.

Development
-----------

Additional development and documentation dependencies can be installed using extras. It is recommended to use a virtualenv.

### Use Pre-Commit Hooks

Install pre-commit hooks and dependencies:

    pip install -e .[dev]
    pre-commit install
    pre-commit autoupdate
    pre-commit run --all-files

### Run Tests

Run tests from the source with Pytest:

    pip install -e .[dev]
    pytest -s

### Generate Documentation

Generate documentation from the source with Sphinx:

    pip install -e .[docs]
    cd docs
    mkdir -p _static _templates
    make html
    python -m http.server --directory build/html

QueueListenerHandler
--------------------

A simple `QueueHandler` subclass implementation utilizing `QueueListener` for configured handlers. This is helpful for detaching the logger handlers from the main threads, which reduces the risk of getting blocked, for example, when using slower handlers such as smtp, file, or socket handlers.

### Example configuration:

File: [logging.yaml](./docs/snippets/logging.yaml)
```
version: 1
objects:
  queue:
    class: queue.Queue
    maxsize: 1000
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    stream: ext://sys.stdout
  file_handler:
    class: logging.FileHandler
    filename: 'test_logger.log'
    formatter: simple
  queue_handler:
    class: logging_.QueueListenerHandler
    handlers:
      - cfg://handlers.console
      - cfg://handlers.file_handler
    queue: cfg://objects.queue
loggers:
  test_logger:
    level: DEBUG
    handlers:
      - queue_handler
    propagate: yes
root:
  level: NOTSET
  handlers:
    - console
```

**Note:** A queue object must be passed since the handler does not set a default queue implementation. Set `maxsize: -1` to make the queue unlimited.

### Example Usage

Just load the configuration file and start logging.

File: [test_logger.py](./docs/snippets/test_logger.py)
```
import logging.config
import yaml

with open("logging.yaml", "r") as config_file:
    logging_config = yaml.safe_load(config_file.read())
    logging.config.dictConfig(logging_config)

logger = logging.getLogger(__name__)

logger.debug("This is a debug log")
logger.info("This is an info log")
logger.warning("This is an warning log")
logger.error("This is an error log")
logger.critical("This is a critical log")
```

### Sources

1. `QueueListenerHandler` was inspired by [Rob Blackbourn's implementation](https://rob-blackbourn.medium.com/how-to-use-python-logging-queuehandler-with-dictconfig-1e8b1284e27a).
