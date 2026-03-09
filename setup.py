from setuptools import setup, find_namespace_packages

setup(
    name="me-v2",
    version="0.1",
    packages=find_namespace_packages(),
    install_requires=[
        "chromadb",
        "requests",
        "rich",
        "InquirerPy",
    ],
    entry_points={
        "console_scripts": [
            "me-v2=cli.main:main",
        ],
    },
)