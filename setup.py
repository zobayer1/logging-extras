# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = "\n" + f.read()

setup(
    name="logging-extras",
    url="https://github.com/zobayer1/logging-extras",
    license="MIT",
    author="Zobayer Hasan",
    author_email="zobayer1@gmail.com",
    description="Python logging extensions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="python logging logger handler custom config dictconfig yaml",
    packages=find_packages(exclude=["docs", "tests"]),
    use_scm_version=True,
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
