# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 8):  # pragma: no cover
    # noinspection PyUnresolvedReferences
    from importlib_metadata import version
else:  # pragma: no cover
    from importlib.metadata import version

__version__ = version("logging-extras")
