from setuptools import find_packages, setup

setup(
    name="custom_cli",
    version="0.1",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={"console_scripts": ["cli=cli.main:main"]},
)
