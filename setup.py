from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def run_tests(self):
        import pytest

        errno = pytest.main(["-s"])
        sys.exit(errno)


setup(
    name='fntlib',
    packages=find_packages(include=['fntlib']),
    version='1.0.0',
    description='A Python library to work with bitmap .fnt font files.',
    author='Jaan',
    license='MIT',
    url='https://github.com/JaanDev/fntlib',
    keywords='python library font fnt bitmap fonts interaction',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    cmdclass={
        'pytest': PyTest,
    },
    long_description='''Ok test desc here'''
)