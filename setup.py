import flagparse

import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file.
with open(os.path.join(here, "README.md"), encoding="utf-8") as md:
    long_description = md.read()


setuptools.setup(
    name="flagparse",
    version=flagparse.__version__,

    long_description=long_description,
    long_description_content_type="text/markdown",
    description="flagparse is library to parse flags",

    url="https://github.com/ybubnov/flagparse",
    author="Yasha Bubnov",
    author_email="girokompass@gmail.com",

    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ],

    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        "enum",
    ],
)
