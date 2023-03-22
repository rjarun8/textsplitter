import re
import string
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import tiktoken

class TextSplitter:
    def __init__(self, max_token_size=3500, end_sentence=True, preserve_formatting=True,
                 remove_urls=True, replace_entities=True, remove_stopwords=True, language='english'):
        self.max_token_size = max_token_size
        self.end_sentence = end_sentence
        self.preserve_formatting = preserve_formatting
        self.remove_urls = remove_urls
        self.replace_entities = replace_entities
        self.remove_stopwords = remove_stopwords
        self.language = language
        self.encoding = tiktoken.get_encoding("gpt2")

    def split_text(self, text):
        tokens = self.encoding.encode(text)
        num_tokens = len(tokens)

        if num_tokens <= self.max_token_size:
            return [text]

        chunks = self._split_tokens_into_chunks(tokens, num_tokens)
        return self._process_chunks(chunks)

    def _split_tokens_into_chunks(self, tokens, num_tokens):
        num_chunks = (num_tokens + self.max_token_size - 1) // self.max_token_size
        chunk_size = num_tokens // num_chunks

        chunks = []
        start = 0
        for _ in range(num_chunks):
            end = min(start + chunk_size, num_tokens)

            if self.end_sentence:
                while end < num_tokens and not self._is_end_of_sentence(tokens[end]):
                    end += 1

                # If no period is found, use the original end index
                if end >= num_tokens:
                    end = num_tokens

            chunks.append(tokens[start:end])

            # Move the start to the next token after the end-of-sentence token
            start = end + 1 if end < num_tokens and self._is_end_of_sentence(tokens[end]) else end

        return chunks



    def _adjust_end_index(self, tokens, end, num_tokens):
        while end < num_tokens and not self._is_end_of_sentence(tokens[end]):
            end += 1

        # If no period is found, return the original end index
        if end >= num_tokens:
            return num_tokens

        return end


    

    def _process_chunks(self, chunks):
        processed_chunks = []
        for chunk_tokens in chunks:
            chunk_text = self.encoding.decode(chunk_tokens)
            chunk_text = self._preserve_formatting(chunk_text)
            chunk_text = self._remove_urls(chunk_text)
            chunk_text = self._replace_entities(chunk_text)
            chunk_text = self._remove_stopwords(chunk_text)

            if chunk_text.strip():  # Only add non-empty chunks to the list
                processed_chunks.append(chunk_text)
        return processed_chunks


    def _preserve_formatting(self, chunk_text):
        if not self.preserve_formatting:
            return chunk_text

        if not re.match(r'^\s', chunk_text):
            chunk_text = ' ' + chunk_text
        chunk_text = re.sub(r'\s+', ' ', chunk_text)
        return chunk_text.strip()

    def _remove_urls(self, chunk_text):
        if not self.remove_urls:
            return chunk_text

        chunk_text = re.sub(r'http\S+', '', chunk_text)
        return re.sub(r'www\S+', '', chunk_text)

    def _replace_entities(self, chunk_text):
        if not self.replace_entities:
            return chunk_text

        return re.sub(r'<[^>]+>', ' ', chunk_text)

    def _remove_stopwords(self, chunk_text):
        if not self.remove_stopwords:
            return chunk_text

        stop_words = set(stopwords.words(self.language))
        words = word_tokenize(chunk_text)
        return ' '.join(w for w in words if w.lower() not in stop_words)


    def _is_end_of_sentence(self, token):
        return self.encoding.decode([token]).strip().endswith('.')
    