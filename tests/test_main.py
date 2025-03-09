import unittest
from codesearchtool import CodeSearchTool

class TestCodeSearchTool(unittest.TestCase):
    def setUp(self):
        self.tool = CodeSearchTool('path_to_test_code_repository')

    def test_search(self):
        query = 'How to open a file in Python?'
        language = 'py'
        results = self.tool.search(query, language)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

if __name__ == '__main__':
    unittest.main()