import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

class CodeSearchTool:
    """
    A tool for searching a local repository of code snippets based on natural language queries.
    """

    def __init__(self, repository_path: str):
        """
        Initialize the tool with the path to the local repository of code snippets.

        :param repository_path: The path to the local repository of code snippets.
        """
        self.repository_path = repository_path
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.code_snippets = self.load_code_snippets()

    def load_code_snippets(self) -> dict:
        """
        Load code snippets from the local repository.

        :return: A dictionary where keys are file names and values are code snippets.
        """
        code_snippets = {}
        for file_name in os.listdir(self.repository_path):
            with open(os.path.join(self.repository_path, file_name), 'r') as file:
                code_snippets[file_name] = file.read()
        return code_snippets

    def process_query(self, query: str) -> str:
        """
        Process a natural language query using NLP techniques.

        :param query: A natural language query.
        :return: A processed query.
        """
        return nltk.word_tokenize(query)

    def search(self, query: str) -> dict:
        """
        Search the local repository of code snippets based on a processed query.

        :param query: A processed query.
        :return: A dictionary where keys are file names and values are relevance scores.
        """
        tfidf_matrix = self.vectorizer.fit_transform(list(self.code_snippets.values()) + [query])
        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
        return {file_name: similarity for file_name, similarity in zip(self.code_snippets.keys(), cosine_similarities)}

    def recommend(self, query: str) -> dict:
        """
        Recommend relevant code snippets based on a processed query.

        :param query: A processed query.
        :return: A dictionary where keys are file names and values are relevance scores.
        """
        processed_query = self.process_query(query)
        search_results = self.search(processed_query)
        return {k: v for k, v in sorted(search_results.items(), key=lambda item: item[1], reverse=True)}

# Example usage:
tool = CodeSearchTool('/path/to/repository')
recommendations = tool.recommend('How do I write a for loop in Python?')
for file_name, relevance_score in recommendations.items():
    print(f'{file_name}: {relevance_score}')