from setuptools import setup

setup(
    name="fillmydb",
    version="0.1.0",
    description="Fill your database with mocked instances.",
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
