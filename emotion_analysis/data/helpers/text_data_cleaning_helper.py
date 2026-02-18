from typing import TYPE_CHECKING, Set
from wordcloud import STOPWORDS

if TYPE_CHECKING:
    from emotion_analysis.data.ea_data_cleaning import EATextDataCleaning

class TextDataCleaningHelper:
    @staticmethod
    def clean_text(text: str, cleaner: "EATextDataCleaning", stopwords: Set[str] = STOPWORDS):
        url_removed_text = cleaner.remove_urls(text)
        lowered_text = cleaner.to_lowercase(url_removed_text)
        punctuation_removed_text = cleaner.remove_punctuation(lowered_text)
        stopwords_removed_text = cleaner.remove_stopwords(punctuation_removed_text, stopwords)
        lemmatized_text = cleaner.lemmatize(stopwords_removed_text)
        
        return lemmatized_text
        
        