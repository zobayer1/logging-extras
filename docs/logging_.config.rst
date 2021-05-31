Config
------

YAMLConfig
++++++++++

``YAMLConfig`` class can be used for loading YAML files with custom tags. This class adds a custom envvar tag to native YAML parser which is used to evaluate environment variables. Supports one or more environment variables in the form of ``${VARNAME}`` or ``${VARNAME:DEFAULT}`` within a string. If no default value is specified, empty string is used. Default values can only be treated as plain strings.

Example Usage
*************

An example YAML configuration file with environment variables:

.. literalinclude:: snippets/yaml_config/logging.yaml
   :caption: logging.yaml
   :language: yaml
   :emphasize-lines: 12

Load the file with YAMLConfig and start logging:

.. literalinclude:: snippets/yaml_config/test_logger.py
   :caption: test_logger.py
   :language: python

Optional Params
***************

An explicit ``silent=True`` flag must be set to suppress any file or parsing related exceptions to be thrown.

Regex Matchers
**************

Regex used for parsing environment variables: ``r"\${([^}^{]+)}"``. Allowed patterns: ``${VARNAME}``, ``${VARNAME:DEFAULT}``, ``${VARNAME:}``.

Module Members
++++++++++++++

.. automodule:: logging_.config.yaml_config
   :members:
   :special-members:
   :show-inheritance:
