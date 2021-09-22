# -*- coding: utf-8 -*-
import pytest

import logging_


def test_version():
    """Test fails if version string for package could not be fetched"""
    assert len(logging_.__version__) > 0
