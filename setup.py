from setuptools import setup, find_packages

setup(
    name="lmrtask",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "flet"
    ],
    entry_points={
        "console_scripts": [
            "lmrtask=lmrtask.main:main"
        ]
    }
)
