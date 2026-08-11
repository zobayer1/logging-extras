v1.0.0 (2026-08-11)
+++++++++++++++++++

First stable release. The library's scope is considered complete: YAML-based logging configuration
plus a ``QueueListenerHandler`` backport for Python versions that predate the standard library's
native queue support.

Changes

* Fix ``AttributeError`` raised at interpreter shutdown when a ``QueueListenerHandler`` listener had
  already been stopped manually. ``QueueListener.stop()`` is not idempotent on Python < 3.13, so the
  ``atexit``-registered callback failed on the second call. ``QueueListenerHandler`` now exposes an
  idempotent ``stop()`` that unregisters its ``atexit`` callback and only stops a listener whose
  thread is still running.
* Document ``QueueListenerHandler`` as a backport for Python 3.8 - 3.11 and point users on Python
  3.12+ to the standard library's native ``dictConfig`` queue support.
* Publish to PyPI via `Trusted Publishing (OIDC)
  <https://docs.pypi.org/trusted-publishers/>`_ instead of stored ``PYPI_USERNAME`` / ``PYPI_PASSWORD``
  secrets. The ``.github/workflows/python-publish.yml`` job now requests an OIDC token
  (``permissions: id-token: write``) and publishes through ``pypa/gh-action-pypi-publish``. No
  long-lived credentials are required in the repository secrets.
* Promote the ``Development Status`` classifier from ``4 - Beta`` to ``5 - Production/Stable``.

v0.4.0-beta (2026-07-22)
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
