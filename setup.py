try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requirements = [
    'lxml',
    'libxml2',
    'bs4',
    'beautifulsoup4',
    'python-dateutil'
]

setup(
    name='email_parser',
    version='0.1.0',
    author='haruka',
    url='https://github.com/haruka-YNU/email_parser',
    author_email='xiao-yao-tn@ynu.jp',
    py_modules=['email_parser'],
    license='MIT',
    install_requires = requirements
)
