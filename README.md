# Text Splitter

A Python library to split large text into smaller chunks based on the maximum token size and other criteria.

## Features

- Split text into smaller chunks based on maximum token size
- End chunks at sentence boundaries
- Preserve formatting
- Remove URLs
- Replace entities
- Remove stopwords

## Installation

To install the library, run the following command:

pip install textsplitter


## Usage

Here's a simple example of how to use the TextSplitter:

```python
from textsplitter import TextSplitter

sample_text = "Your sample text goes here..."

text_splitter = TextSplitter(max_token_size=20, end_sentence=True, preserve_formatting=True,
                             remove_urls=True, replace_entities=True, remove_stopwords=True, language='english')

chunks = text_splitter.split_text(sample_text)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}:\n{chunk}")
