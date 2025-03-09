import os
import re
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')
nltk.download('stopwords')

class CodeSearchTool:
    """
    A tool for searching a local repository of code snippets based on natural language queries.
    """
    def __init__(self, repo_path: str):
        """
        Initialize the tool with the path to the code repository.
        """
        self.repo_path = repo_path
        self.vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'))

    def _load_snippets(self, language: str) -> List[str]:
        """
        Load all code snippets in the specified programming language.
        """
        snippets = []
        for filename in os.listdir(self.repo_path):
            if filename.endswith('.' + language):
                with open(os.path.join(self.repo_path, filename), 'r') as file:
                    snippets.append(file.read())
        return snippets

    def _preprocess_query(self, query: str) -> str:
        """
        Preprocess the query by removing punctuation and converting to lowercase.
        """
        query = re.sub(r'\W', ' ', query)
        query = query.lower()
        return query

    def search(self, query: str, language: str) -> List[Tuple[str, float]]:
        """
        Search the code repository based on the query and programming language.
        """
        query = self._preprocess_query(query)
        snippets = self._load_snippets(language)

        tfidf_matrix = self.vectorizer.fit_transform([query] + snippets)
        cosine_similarities = (tfidf_matrix * tfidf_matrix.T).A[0]

        ranked_snippets = sorted(zip(snippets, cosine_similarities[1:]), key=lambda x: -x[1])
        return ranked_snippets


if __name__ == "__main__":
    tool = CodeSearchTool('path_to_your_code_repository')
    results = tool.search('How to open a file in Python?', 'py')
    for snippet, score in results:
        print(f'Score: {score}\nSnippet:\n{snippet}\n')