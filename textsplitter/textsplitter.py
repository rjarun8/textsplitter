import re
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import tiktoken

class TextSplitter:
    def __init__(self, max_token_size=3500, end_sentence=True, preserve_formatting=True, remove_urls=True, replace_entities=True, remove_stopwords=True, language='english'):
        self.max_token_size = max_token_size
        self.end_sentence = end_sentence
        self.preserve_formatting = preserve_formatting
        self.remove_urls = remove_urls
        self.replace_entities = replace_entities
        self.remove_stopwords = remove_stopwords
        self.language = language
        self.encoding = tiktoken.get_encoding("gpt2")

    def split_text(self, text):
        try:
            tokens = self.encoding.encode(text)
            num_tokens = len(tokens)

            # If the text is already within the token size limit, return it as is
            if num_tokens <= self.max_token_size:
                return [text]

            # Otherwise, split the text into smaller chunks based on the max token size
            num_chunks = (num_tokens + self.max_token_size - 1) // self.max_token_size
            chunk_size = num_tokens // num_chunks

            chunks = []
            start = 0
            for i in range(num_chunks):
                # Determine the end index of the current chunk
                end = min(start + chunk_size, num_tokens)

                # Adjust the end index to ensure that the chunk ends at a token boundary
                if self.end_sentence:
                    while end < num_tokens and not self.is_end_of_sentence(tokens[end]):
                        end += 1

                # Add the current chunk to the list of chunks
                chunk_tokens = tokens[start:end]
                chunk_text = self.encoding.decode(chunk_tokens)

                # Preserve formatting (e.g., line breaks, whitespace) if desired
                if self.preserve_formatting:
                    # Add whitespace at the beginning of the chunk if it starts with a non-whitespace character
                    if not re.match(r'^\s', chunk_text):
                        chunk_text = ' ' + chunk_text

                    # Replace multiple consecutive whitespace characters with a single space
                    chunk_text = re.sub(r'\s+', ' ', chunk_text)

                    # Remove whitespace at the end of the chunk
                    chunk_text = chunk_text.strip()

                # Remove URLs if desired
                if self.remove_urls:
                    chunk_text = re.sub(r'http\S+', '', chunk_text)
                    chunk_text = re.sub(r'www\S+', '', chunk_text)

                # Replace entities (e.g., <br>) with whitespace if desired
                if self.replace_entities:
                    chunk_text = re.sub(r'<[^>]+>', ' ', chunk_text)

                # Remove stopwords if desired
                if self.remove_stopwords:
                    stop_words = set(stopwords.words(self.language))
                    words = word_tokenize(chunk_text)
                    words = [w for w in words if not w.lower() in stop_words]
                    chunk_text = ' '.join(words)

                chunks.append(chunk_text)
                start = end

            return chunks

        except Exception as e:
            print("Error occurred during text splitting:", e)

    def is_end_of_sentence(self, token):
        return self.encoding.decode([token]).strip().endswith('.')
