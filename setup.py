from setuptools import setup, find_packages

setup(
    name='codesnippetrecommender',
    version='0.1.0',
    description='A tool that recommends relevant code snippets based on natural language queries.',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'nltk==3.6.2',
        'scikit-learn==0.24.2',
        'requests==2.25.1',
    ],
)