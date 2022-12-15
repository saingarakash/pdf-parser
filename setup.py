from setuptools import find_packages, setup

setup(
    name="pdf-parser",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "python",
        "PyDrive",
        "dateparser",
        "pdfminer.six",
        "thefuzz",
        "python-Levenshtein",
        "openpyxl",
        "lxml",
        "PyPDF2",
        "defusedxml",
    ],
)
