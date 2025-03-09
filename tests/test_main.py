import unittest
from codesnippetrecommender import CodeSnippetRecommender

class TestCodeSnippetRecommender(unittest.TestCase):

    def setUp(self):
        self.recommender = CodeSnippetRecommender('snippets_dir', 'metadata.json')

    def test_process_query(self):
        query = 'How do I write a function in Python to sort a list?'
        expected_result = ['How', 'do', 'I', 'write', 'a', 'function', 'in', 'Python', 'to', 'sort', 'a', 'list', '?']
        self.assertEqual(self.recommender.process_query(query), expected_result)

    def test_recommend_snippets(self):
        query = 'How do I write a function in Python to sort a list?'
        result = self.recommender.recommend_snippets(query)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()