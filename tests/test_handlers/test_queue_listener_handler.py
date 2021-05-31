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


@pytest.fixture(scope="module")
def logger():
    """Fixture for providing a configured logger object"""
    logging_config = yaml.safe_load(config_yaml)
    logging.config.dictConfig(logging_config)
    return logging.getLogger("test_logger")


def test_logger_emits_with_queue_handler(logger, caplog):
    """Test fails if queue handler could not emit logs"""
    logger.info("This is a test")
    assert "This is a test" in caplog.text
