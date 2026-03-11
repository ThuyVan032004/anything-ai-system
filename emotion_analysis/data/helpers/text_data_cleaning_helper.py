import re
import string
from typing import TYPE_CHECKING, Set
from wordcloud import STOPWORDS
from nltk.stem import WordNetLemmatizer

# if TYPE_CHECKING:
#     from emotion_analysis.data.ea_data_cleaning import EATextDataCleaning

lemmatizer = WordNetLemmatizer()

class TextDataCleaningHelper:
    @staticmethod
    def clean_text(text, stopwords=STOPWORDS):
        # Lower
        text = text.lower()

        # Remove punctuation
        text = text.translate(str.maketrans('','', string.punctuation))

        # Remove stopwords
        splitted_words = text.split()
        words = [word for word in splitted_words if word not in stopwords]
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

        lemmatized_text = ' '.join(lemmatized_words)

        # Remove URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        cleaned_text = re.sub(url_pattern, '', lemmatized_text)

        return cleaned_text
        