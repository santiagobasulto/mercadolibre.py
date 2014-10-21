import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

VERSION = "0.1.7"


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-m', 'not integration', '--cov',
                            'mercadolibre', 'tests/']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import sys, pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def extract_requirements(lines):
    return [l.replace('\n', '') for l in lines if
            l and not l.startswith('-r ') and not l == '\n']


setup(
    name='mercadolibre.py',
    version=VERSION,
    description='Mercadolibre Python SDK (for humans)',
    author='Santiago Basulto',
    author_email="santiago.basulto@gmail.com",
    packages=['mercadolibre'],
    url='https://github.com/santiagobasulto/mercadolibre.py',
    download_url=("https://github.com/santiagobasulto/"
                  "mercadolibre.py/tarball/"
                  "{version}".format(version=VERSION)),
    include_package_data=True,
    install_requires=['requests>=2.0'],
    tests_require=[
        'click==3.2',
        'cov-core==1.14.0',
        'coverage==3.7.1',
        'pytest==2.6.1',
        'pytest-cov==1.8.0',
        'six==1.7.3',
        'mock==1.0.1',
        'tox==1.7.2',
        'vcrpy==1.0.3',
    ],
    license='MIT',
    zip_safe=False,
    cmdclass={'test': PyTest},
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)
