# -*- coding: utf-8 -*-
import logging.config
import os
import re
from os.path import realpath, splitext, join as join_path, curdir, isfile, abspath, commonpath
from typing import Any, Union, TextIO, Optional

import yaml
from yaml.parser import ParserError


class YAMLConfig(object):
    """YAMLConfig class for loading YAML configurations with custom tagging and transformation rules.

    This class adds a custom envvar tag to native YAML parser which is used to evaluate environment variables. Supports
    one or more environment variables in the form of ``${VARNAME}`` or ``${VARNAME:DEFAULT}`` within a string. If no
    default value is specified, empty string is used. Default values can only be treated as plain strings. YAMLConfig
    can also expand ``~`` or ``~user`` just like shells do, either directly hardcoded in YAML file or passed through
    environment variables.Inspired by several examples from programcreek:
    ``https://www.programcreek.com/python/example/11269/yaml.add_constructor``.

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
    _uservar_tag_matcher = re.compile(r"^~(\w*?)/")

    def __init__(self, config_yaml: Union[TextIO, str], rootpath: Optional[str] = None, unsafe: bool = False, include: bool = True, **kwargs: Any):
        """Instantiates an YAMLConfig object from configuration string.

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
        self.include = include
        self.unsafe = unsafe
        self._rootpath = rootpath

        if not self._rootpath:
            self._rootpath = realpath(curdir)
        yaml.add_implicit_resolver("!envvar", self._envvar_tag_matcher, None, yaml.SafeLoader)
        yaml.add_constructor("!envvar", self._envvar_constructor, yaml.SafeLoader)
        yaml.add_implicit_resolver("!uservar", self._uservar_tag_matcher, None, yaml.SafeLoader)
        yaml.add_constructor("!uservar", self._uservar_constructor, yaml.SafeLoader)
        yaml.add_constructor("!include", self._ctor_include, yaml.SafeLoader)  # noqa
        try:
            logging.config.dictConfig(yaml.safe_load(config_yaml))
        except (ParserError, ValueError, TypeError):
            if kwargs.get("silent", False) is not True:
                raise

    def safe_path(self, child_path: str, allow_symlinks: bool = True):
        """Security check: ensure that a file is at or below the directory path of the primary YaML file

        Parameters
        ----------
        child_path : str
            Path of the file to be included
        allow_symlinks : bool, default=True
            If True, don't resolve symlinks

        Returns
        -------
        bool
            True if safe, False if unsafe
        """
        root_path = abspath(self._rootpath)
        child_path = abspath(child_path)
        if allow_symlinks is False:
            root_path = realpath(root_path)
            child_path = realpath(child_path)
        return commonpath([root_path]) == commonpath([root_path, child_path])

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
            with open(filename, "r") as fd:
                return cls(fd.read(), **kwargs)
        except (FileNotFoundError, PermissionError):
            if kwargs.get("silent", False) is not True:
                raise
            return cls("", **kwargs)

    def _envvar_constructor(self, _loader: Any, node: Any):
        """Replaces environment variable name with its value, or a default."""

        def replace_fn(match):
            envparts = f"{match.group(1)}:".split(":")
            return os.environ.get(envparts[0], envparts[1])

        return os.path.expanduser(self._envvar_sub_matcher.sub(replace_fn, node.value))

    @staticmethod
    def _uservar_constructor(_loader: Any, node: Any):
        """Expands ~ and ~username into user's home directory like shells do."""
        return os.path.expanduser(node.value)

    def _ctor_include(self, _loader: Any, node: Any) -> Any:
        """Dynamically load the contents of an external YaML or flat file in-place

        Notes
        -----
        Invoked internally via PyYaML when encountering a custom include tag

        Parameters
        ----------
        node:
            PyYaML YaML node object

        Returns
        -------
        Any
            If node.value has a yaml/yml extension, structured data from the specified YaML file
            If node.value has a list/lst extension, a list of strings, one per-line in the specified file
            Otherwise, the contents of the specified file, with newlines removed
        """
        if self.include is False:
            raise RuntimeError('Attempting to use !include when includes are explicitly disabled!')
        base_file = _loader.construct_scalar(node)
        include_file = realpath(join_path(self._rootpath, base_file))
        extension = splitext(include_file)[1].lstrip('.').lower()

        if self.unsafe is False and not self.safe_path(include_file):
            # Use the UnsafeExtLoader to get around this check
            raise RuntimeError(f'Trying to include unsafe YaML file (outside of root directory {self._rootpath})')

        print('Trying to include file %s @ %s' % (base_file, include_file))
        if not isfile(include_file):
            include_file = join_path(self._rootpath, 'include', base_file)
            print('Trying to find %s @ %s' % (base_file, include_file))
            if not isfile(include_file):
                raise OSError(f'Unable to find include file {base_file}')

        with open(include_file, mode='r') as fd:
            # If YaML, load as YaML; otherwise load the file contents as a scalar string value, trimming out newlines
            if extension.lower() in ('yml', 'yaml'):
                # Return as fully structured data
                return yaml.load(fd, yaml.SafeLoader)
            if extension.lower() in ('lst', 'list'):
                # File is a flat list with one element per-line
                # Return as a list object, preserving order, filtering out blank lines / whitespace-only lines
                # Also skip lines starting with '#' to support comments in flat list files
                return [line for line in fd.read().splitlines() if line.strip() and not line.startswith('#')]
            # Fallback: Return a single line blob, removing newlines if there are any
            return ''.join(fd.readlines())
