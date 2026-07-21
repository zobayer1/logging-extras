# -*- coding: utf-8 -*-
import logging.config

import pytest
import yaml

config_yaml = """
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
  queue_handler:
    class: logging_.handlers.QueueListenerHandler
    handlers:
      - cfg://handlers.console
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
"""


@pytest.fixture(scope="function")
def logger():
    """Fixture for providing a configured logger object"""
    logging_config = yaml.safe_load(config_yaml)
    logging.config.dictConfig(logging_config)
    return logging.getLogger("test_logger")


def test_logger_emits_with_queue_handler(logger, caplog):
    """Test fails if queue handler could not emit logs"""
    logger.info("This is a test")
    assert "This is a test" in caplog.text


def test_queue_listener_handler_is_not_a_queuehandler_subclass():
    """Regression: subclassing ``QueueHandler`` triggers dictConfig's native intercept on Python 3.12+.

    Keeping ``QueueListenerHandler`` a plain ``logging.Handler`` is what lets the same YAML config work on
    Python 3.8-3.15. If this ever fails, the handler will break under ``dictConfig`` on Python 3.12+.
    """
    from logging.handlers import QueueHandler

    from logging_.handlers import QueueListenerHandler

    assert issubclass(QueueListenerHandler, logging.Handler)
    assert not issubclass(QueueListenerHandler, QueueHandler)


def test_queue_listener_handler_auto_run_false_does_not_start_listener():
    """Test fails if ``auto_run=False`` starts the queue listener thread."""
    import queue as queue_module

    from logging_.handlers import QueueListenerHandler

    handler = QueueListenerHandler(queue_module.Queue(-1), [], auto_run=False)
    assert handler._listener._thread is None
