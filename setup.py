import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


long_description = read('README.md') if os.path.isfile("README.md") else ""

setup(
    name='blockchain-etl-table-definition-cli',
    version='1.3.0',
    author='Evgeny Medvedev',
    author_email='evge.medvedev@gmail.com',
    description='Tools for generating table definitions for https://github.com/blockchain-etl/ethereum-etl-airflow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blockchain-etl/blockchain-etl-table-definition-cli',
    packages=find_packages(exclude=['schemas', 'tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='ethereum,polygon,bsc,arbitrum,fantom,celo,ronin,avalanche',
    python_requires='>=3.5.3,<4',
    install_requires=[
        'click==7.0'
    ],
    entry_points={
        'console_scripts': [
            'tabledefinition=tabledefinition.cli:cli',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/blockchain-etl/blockchain-etl-table-definition-cli/issues',
        'Chat': 'https://gitter.im/ethereum-etl/Lobby',
        'Source': 'https://github.com/blockchain-etl/blockchain-etl-table-definition-cli',
    },
)
