"""Setup using distutils."""

import os

from setuptools import setup


def read(fname):
    """Read file relative to setup.py's location."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()


setup(
    name="httpie-gridscale-auth",
    version="1.0.0",
    author="ghostwheel42",
    description="gridscale auth plugin for HTTPie.",
    license="MIT",
    keywords="",
    url="https://github.com/ghostwheel42/httpie-gridscale-auth",
    long_description=read("README.md"),
    py_modules=["httpie_gridscale_auth"],
    zip_safe=False,
    entry_points={
        "httpie.plugins.auth.v1": [
            "httpie_gridscale_auth = httpie_gridscale_auth:GSAuthPlugin"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
)
