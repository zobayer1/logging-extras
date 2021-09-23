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
    filename: ${LOG_FILENAME:test_logger.log}
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

config_yaml_expand_user = """
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
    filename: ~/test_logger.log
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


@pytest.fixture(scope="function")
def logger():
    """Fixture for providing a configured logger object"""
    YAMLConfig(config_yaml)
    return logging.getLogger("test_logger")


def test_logger_configured_with_yaml_config(logger, caplog):
    """Test fails if logger can not be configured with envvars in YAML"""
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            assert "test_logger.log" in handler.baseFilename
    logger.info("This is a test")
    assert "This is a test" in caplog.text


def test_logger_configured_with_yaml_config_raises():
    """Test fails if empty YAML configuration does not raise error when silent=False"""
    with pytest.raises(TypeError):
        YAMLConfig("", silent=False)


def test_logger_configured_with_yaml_file(fs):
    """Test fails if YAMLConfig cannot be instantiated from Yaml file"""
    fs.create_dir(os.path.expanduser("~"))
    fs.create_file("logging.yaml", contents=config_yaml)
    YAMLConfig.from_file("logging.yaml")
    logger = logging.getLogger("test_logger")
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            assert "test_logger.log" in handler.baseFilename


def test_logger_configuration_raises_for_invalid_file():
    """Test fails if YAMLConfig does not raise error when invalid config file given"""
    with pytest.raises(FileNotFoundError):
        YAMLConfig.from_file("logging.yaml")


def test_logger_configuration_silently_ignores_invalid_file():
    """Test fails if YAMLConfig raises error for invalid config file when silent=True"""
    YAMLConfig.from_file("logging.yaml", silent=True)


def test_logger_configuration_expands_user(fs):
    """Test fails if YAMLConfig cannot parse ~ or ~username like shells do"""
    fs.create_dir(os.path.expanduser("~"))
    YAMLConfig(config_yaml_expand_user)
    logger = logging.getLogger("test_logger")
    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            assert "test_logger.log" in handler.baseFilename
