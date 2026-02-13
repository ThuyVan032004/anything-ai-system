import re
import string
from typing import List, Set
from nltk.stem import WordNetLemmatizer, PorterStemmer
from shared.src.data.interfaces.i_text_data_cleaning import ITextDataCleaning


class TextDataCleaningBase(ITextDataCleaning):
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer() # Placeholder for lemmatizer if needed
        
    def to_lowercase(self, text: str) -> str:
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_stopwords(self, text: str, stopwords: List[str] | Set[str]) -> str:
        words = text.split()
        filtered_words = [word for word in words if word not in stopwords]
        return ' '.join(filtered_words)
    
    def stem(self, text: str) -> str:
        words = text.split()
        stemmed_words = [self.stemmer.stem(word) for word in words]
        return ' '.join(stemmed_words)
    
    def lemmatize(self, text: str) -> str:
        words = text.split()
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)
    
    def remove_whitespace(self, text: str) -> str:
        return ' '.join(text.split())
    
    def remove_urls(self, text: str) -> str:
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)