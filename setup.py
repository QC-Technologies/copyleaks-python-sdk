from setuptools import find_packages
from distutils.core import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='CopyleaksPythonSDK',
    packages=find_packages(exclude=['tests*']),
    version='0.1',
    description='A Python SDK for Copyleaks (http://copyleaks.com)',
    long_description=readme(),
    author='Waqas Younas',
    author_email='waqas.younas@gmail.com',
    url = 'https://github.com/wyounas/copyleaks-python-sdk', # use the URL to the github repo
    keywords=['copyleaks', 'copyleakssdk', 'sdk'],
    install_requires=[
        'requests',
        'retrying'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.7',
    ]
)

