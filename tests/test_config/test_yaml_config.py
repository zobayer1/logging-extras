# -*- coding: utf-8 -*-
import logging
import os

import pytest

from logging_.config import YAMLConfig

config_yaml = """
    version: 1
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
        filename: ${LOGGING_ROOT:.}/${LOG_FILENAME}
        formatter: simple
    loggers:
      test_logger:
        level: DEBUG
        handlers:
          - file_handler
        propagate: yes
    root:
      level: NOTSET
      handlers:
        - console
"""


@pytest.fixture(scope="module")
def logger():
    """Fixture for providing a configured logger object"""
    os.environ.update({"LOG_FILENAME": "test_logger.log"})
    YAMLConfig(config_yaml)
    return logging.getLogger("test_logger")


def test_logger_configured_with_yaml_config(logger, caplog):
    """Test fails if logger can not be configured with envvars in YAML"""
    log_file_name = os.environ.get("LOG_FILENAME")
    file_handler = None
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            file_handler = handler
            break
    assert log_file_name in file_handler.baseFilename
    logger.error("This is a test")
    assert "This is a test" in caplog.text


def test_logger_configured_with_yaml_config_raises():
    """Test fails if empty YAML configuration does not raise error when silent=False"""
    with pytest.raises(TypeError):
        YAMLConfig("", silent=False)
