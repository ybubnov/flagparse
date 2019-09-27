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
    description="flagparse is library to build command-line interfaces",

    url="https://github.com/ybubnov/flagparse",
    author="Yasha Bubnov",
    author_email="girokompass@gmail.com",

    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    python_requires=">=3.6",
    keywords="arguments cli parse",
    py_modules=["flagparse"],
)
