from collections import Counter
from typing import Optional


class TextDataHelper:
    @staticmethod
    def extract_all_words_from_corpus(corpus: list[str]) -> list[str]:
        words = []
        for text in corpus:
            words.extend(text.lower().split())
        return words
    
    @staticmethod
    def count_word_frequencies(words: list[str], top_n: Optional[int]) -> Counter:
        word_counts = Counter(words)
        
        if top_n is not None:
            return word_counts.most_common(top_n)
        return word_counts
        
        