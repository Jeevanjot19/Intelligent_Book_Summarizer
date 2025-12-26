# backend/chunker.py

import re
from typing import List


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences using regex.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, max_words: int = 500) -> List[str]:
    """
    Split text into chunks of approximately max_words words.
    """
    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        # If adding this sentence exceeds the limit, finalize the chunk
        if current_word_count + word_count > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_word_count = word_count
        else:
            current_chunk.append(sentence)
            current_word_count += word_count

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
