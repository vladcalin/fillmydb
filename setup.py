from setuptools import setup

from fillmydb import __author__, __version__

with open("long_descr.rst", "r") as readme:
    long_description = readme.read()

setup(
    name="fillmydb",
    version=__version__,
    description="Fill your database with mocked instances.",
    long_description=long_description,
    license="MIT",
    author="Calin Vlad",
    author_email="vlad.s.calin@gmail.com",
    url="https://github.com/vladcalin/fillmydb",
    packages=[
        "fillmydb",
        "fillmydb.core",
        "fillmydb.handlers"
    ],

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Database"
    ],

    # tests

    test_suite="tests",
    tests_require=[
        "peewee", "sqlalchemy", "django"
    ],

    # dependencies
    install_requires=[
        "fake-factory"
    ],

    extras_require={
        "peewee": [
            "peewee"
        ],
        "django": [
            "django"
        ],
        "sqlalchemy": [
            "sqlalchemy"
        ]
    }
)
