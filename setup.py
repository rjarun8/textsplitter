from setuptools import setup, find_packages

setup(
    name='textsplitter',
    version='1.0.0',
    description='A flexible and customizable text splitting utility.',
    author='Raj Arun',
    author_email='rjarun8@example.com',
    url='https://github.com/rjarun8/textsplitter',
    packages=find_packages(),
    install_requires=['tiktoken', 'nltk'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
