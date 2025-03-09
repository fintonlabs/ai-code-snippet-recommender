import os
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple

class CodeSnippetRecommender:
    """
    A tool that recommends relevant code snippets based on natural language queries.
    """

    def __init__(self, snippets_dir: str, metadata_file: str):
        """
        Initialize the recommender with the directory containing the code snippets and the metadata file.

        :param snippets_dir: The directory containing the code snippets.
        :param metadata_file: The file containing the metadata for the code snippets.
        """
        self.snippets_dir = snippets_dir
        self.metadata_file = metadata_file
        self.snippets_metadata = self.load_metadata()
        self.vectorizer = TfidfVectorizer()

    def load_metadata(self) -> Dict[str, Dict[str, str]]:
        """
        Load the metadata for the code snippets from the metadata file.

        :return: A dictionary mapping from code snippet file names to their metadata.
        """
        with open(self.metadata_file, 'r') as f:
            return json.load(f)

    def process_query(self, query: str) -> List[str]:
        """
        Process a natural language query into a list of key words.

        :param query: The natural language query.
        :return: A list of key words extracted from the query.
        """
        return nltk.word_tokenize(query)

    def search_repository(self, key_words: List[str]) -> Dict[str, float]:
        """
        Search the repository of code snippets based on the processed query.

        :param key_words: The key words to search for.
        :return: A dictionary mapping from code snippet file names to their relevance scores.
        """
        descriptions = [metadata['description'] for metadata in self.snippets_metadata.values()]
        tfidf_matrix = self.vectorizer.fit_transform(descriptions)
        query_vector = self.vectorizer.transform([' '.join(key_words)])
        cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
        return dict(zip(self.snippets_metadata.keys(), cosine_similarities))

    def rank_snippets(self, relevance_scores: Dict[str, float]) -> List[Tuple[str, Dict[str, str], float]]:
        """
        Rank the code snippets based on their relevance scores.

        :param relevance_scores: The relevance scores for the code snippets.
        :return: A list of tuples, each containing a code snippet file name, its metadata, and its relevance score, sorted by relevance score in descending order.
        """
        ranked_snippets = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
        return [(file_name, self.snippets_metadata[file_name], score) for file_name, score in ranked_snippets]

    def recommend_snippets(self, query: str) -> List[Tuple[str, Dict[str, str], float]]:
        """
        Recommend code snippets based on a natural language query.

        :param query: The natural language query.
        :return: A list of recommended code snippets, each represented by a tuple containing the file name, the metadata, and the relevance score.
        """
        key_words = self.process_query(query)
        relevance_scores = self.search_repository(key_words)
        return self.rank_snippets(relevance_scores)

# Example usage:
recommender = CodeSnippetRecommender('snippets_dir', 'metadata.json')
print(recommender.recommend_snippets('How do I write a function in Python to sort a list?'))