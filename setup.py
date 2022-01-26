#!/usr/bin/env python3
"""Setup file for WebThing WS."""
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="webthing-ws",
    version="0.1.2",
    description="A WebThing WebSocket consumer and API client.",
    long_description=long_description,
    url="https://github.com/home-assistant-ecosystem/webthing-ws",
    download_url="https://github.com/home-assistant-ecosystem/webthing-ws/releases",
    author="Fabian Affolter",
    author_email="fabian@affolter-engineering.ch",
    license="MIT",
    install_requires=[
        "aiohttp>=3.7.4,<4",
        "async_timeout",
    ],
    packages=["webthing_ws"],
    python_requires='>=3.8',
    zip_safe=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
)
