from abc import ABC
from typing import List

from matplotlib import pyplot as plt
from wordcloud import WordCloud
from shared.src.data.helpers.text_data_helper import TextDataHelper
from shared.src.data.interfaces.i_corpus_visualization import ICorpusVisualization


class CorpusVisualizationBase(ICorpusVisualization, ABC):
    def __init__(self, corpus: List[str]):
        self.corpus = corpus
        
    def plot_frequency_distribution(self) -> None:
        words = TextDataHelper.extract_all_words_from_corpus(self.corpus)
        top_word_frequencies = TextDataHelper.count_word_frequencies(words, top_n=10)
        
        words, counts = zip(*top_word_frequencies)
       
        plt.figure(figsize=(10, 6))
        plt.barh(range(len(words)), counts, color='steelblue')
        plt.yticks(range(len(words)), words)
        plt.xlabel('Frequency', fontsize=12)
        plt.ylabel('Words', fontsize=12)
        plt.title(f'Top {self.top_n} Most Frequent Words', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        
        for i, count in enumerate(counts):
            plt.text(count, i, f' {count}', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.show()
    
    def generate_word_cloud(self) -> None:
        # Combine all text into a single string
        text = ' '.join([str(doc).lower() for doc in self.corpus])
        
        if not text.strip():
            print("No text found in corpus")
            return
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        # Display word cloud
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud Visualization', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.show()