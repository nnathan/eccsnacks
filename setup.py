from setuptools import setup, find_packages
import sys


setup(
    name="eccsnacks",
    version="1.0.2",
    url="http://github.com/nnathan/eccsnacks",

    author="Naveen Nathan",
    author_email="eccsnacks@t.lastninja.net",

    description="Reference implementation of Curve25519 and Curve448 (goldilocks) as specified in RFC7748",

    packages=find_packages(),

    install_requires=[],

    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

    keywords = ['curve25519', 'curve448', 'goldilocks', 'rfc7748'],
    classifiers=[
        'License :: Public Domain',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
