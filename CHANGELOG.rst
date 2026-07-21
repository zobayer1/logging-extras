v0.4.0-beta (unreleased)
++++++++++++++++++++++++

Changes

* Support Python 3.8 through 3.15 (dropped 3.6 and 3.7).
* ``QueueListenerHandler`` no longer subclasses ``logging.handlers.QueueHandler``. Since Python 3.12
  ``logging.config.dictConfig`` special-cases ``QueueHandler`` subclasses and takes over their construction,
  which broke this handler. It now subclasses ``logging.Handler`` directly so the same YAML configuration
  works on all supported versions.
* Require ``PyYAML>=5.3`` on Python < 3.10 and ``PyYAML>=6.0`` on Python >= 3.10, so projects on older
  interpreters are not forced to upgrade an existing PyYAML 5.x (older PyYAML cannot install on 3.10+ anyway).

v0.3.0-beta (2021-09-23)
++++++++++++++++++++++++

Changes

* Add support for expanding ``~`` or ``~user`` like shells.

v0.2.0-beta (2021-06-01)
++++++++++++++++++++++++

Changes

* Add ``YAMLConfig`` class under ``config`` package.

v0.1.1-beta (2021-05-29)
++++++++++++++++++++++++

Changes

* Move ``QueueListenerHandler`` under ``handlers`` package.

v0.1.0-beta (2021-05-29)
++++++++++++++++++++++++

* First release.
