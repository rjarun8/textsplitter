from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="textsplitter",
    version="1.0.3",
    author="Raj Arun",
    author_email="rjarun8@example.com",
    description="A Python library to split large text into smaller chunks based on the maximum token size and other criteria",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rjarun8/textsplitter.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "nltk>=3.8.1",
        "tiktoken>=0.3.0",
    ],
)

