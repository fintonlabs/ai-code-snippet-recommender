from setuptools import setup, find_packages

setup(
    name='codesearchtool',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'nltk==3.5',
        'scikit-learn==0.24.1',
        'requests==2.25.1',
    ],
    entry_points={
        'console_scripts': [
            'codesearchtool=codesearchtool:main',
        ],
    },
)