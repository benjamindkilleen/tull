#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

setup(
    name="tull",
    version="0.0.0",
    description="A command-line tool for basic image processing, for making graphics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Benjamin D. Killeen",
    author_email="killeen@jhu.edu",
    url="https://github.com/benjamindkilleen/tull",
    install_requires=[
        "click",
        "rich",
        "numpy",
        "opencv-python",
        "scipy",
        "scikit-image",
        "matplotlib",
    ],
    packages=find_packages(),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "tull = tull.cli:cli",
        ]
    },
)
