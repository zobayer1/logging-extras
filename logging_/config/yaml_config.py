# -*- coding: utf-8 -*-
import os
import re
import logging.config
from typing import Any

import yaml
from yaml.parser import ParserError


class YAMLConfig(object):
    """YAMLConfig class for loading YAML configurations with custom tagging and transformation rules.

    This class adds a custom envvar tag to native YAML parser which is used to evaluate environment variables. Supports
    one or more environment variables in the form of ``${VARNAME}`` or ``${VARNAME:DEFAULT}`` within a string. If no
    default value is specified, empty string is used. Default values can only be treated as plain strings. Inspired by
    several examples from programcreek: ``https://www.programcreek.com/python/example/11269/yaml.add_constructor``

    Example configuration::

        # logging.yaml
        version: 1
        formatters:
          simple:
            format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        handlers:
          file_handler:
            class: logging.FileHandler
            filename: ${LOGGING_ROOT:.}/${LOG_FILENAME:test_logger.log}
            formatter: simple

    """

    _envvar_sub_matcher = re.compile(r"\${([^}^{]+)}")
    _envvar_tag_matcher = re.compile(r"[^$]*\${([^}^{]+)}.*")

    def __init__(self, config_yaml: str, **kwargs: Any):
        """Instantiates an YAMLConfig object from configuation string.

        Registers implicit resolver for custom tag envvar and adds constructor for the tag. Loads logging config from
        parsed dictionary using dictConfig.

        Args:
            config_yaml: Configuration YAML string.
            **kwargs: Optional arguments:
                 ``silent (bool)``: If True, silently ignore YAML errors.

        Raises:
            ParserError: if config_yaml isn't a valid YAML string, ignored if ``silent=True``.
            ValueError: if required fields are missing in YAML string, ignored if ``silent=True``.
            TypeError: if empty YAML string is provided, ignored if ``silent=True``.
        """

        yaml.add_implicit_resolver("!envvar", self._envvar_tag_matcher, None, yaml.SafeLoader)
        yaml.add_constructor("!envvar", self._envvar_constructor, yaml.SafeLoader)
        try:
            logging.config.dictConfig(yaml.safe_load(config_yaml))
        except (ParserError, ValueError, TypeError):
            if kwargs.get("silent", False) is not True:
                raise

    @classmethod
    def from_file(cls, filename: str, **kwargs: Any):
        """Creates an instance from YAML configuration file.

        Args:
            filename: Configuration file path.
            **kwargs: Optional arguments:
                 ``silent (bool)``: If True, silently ignore file errors.

        Returns:
            An YAMLConfig instance.

        Raises:
            FileNotFoundError: if filename is not a valid file path, ignored if ``silent=True``.
            PermissionError: if there is no read permission, ignored if ``silent=True``.
        """

        try:
            with open(filename, "r") as f:
                return cls(f.read(), **kwargs)
        except (FileNotFoundError, PermissionError):
            if kwargs.get("silent", False) is not True:
                raise
            else:
                return cls("", **kwargs)

    def _envvar_constructor(self, _loader: Any, node: Any):
        """Constructor callback method for yaml.

        Replaces environment variable name with its value. If it is not set, default value will be set.

        Args:
              _loader: the Loader object, unused.
              node: the Node object.

        Returns:
            The transformed string.
        """

        def replace_fn(match):
            envparts = f"{match.group(1)}:".split(":")
            return os.environ.get(envparts[0], envparts[1])

        return self._envvar_sub_matcher.sub(replace_fn, node.value)
