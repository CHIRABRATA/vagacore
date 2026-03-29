from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vagacore",
    version="1.0.1",
    author="THE CHIRABRATA",
    description="Intelligent Text Compression & Fact Extraction Engine using NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CHIRABRATA/vagacore",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "spacy>=3.0.0",
    ],
)
