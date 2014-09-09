import os
import sys

VERSION = '0.1.0'

from setuptools import setup
from setuptools.command.test import test as TestCommand


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
    return [l for l in lines if
            l and not l.startswith('-r ') and not l == '\n']


with open('requirements.txt') as f:
    requirements = extract_requirements(f.readlines())

with open('requirements-dev.txt') as f:
    requirements_dev = extract_requirements(f.readlines())


setup(
    name='mercadolibre.py',
    version=VERSION,
    description='Mercadolibre Python SDK (for humans)',
    author='Santiago Basulto',
    author_email="santiago.basulto@gmail.com",
    packages=['mercadolibre'],
    url='https://github.com/santiagobasulto/mercadolibre.py',
    include_package_data=True,
    install_requires=requirements,
    tests_require=requirements_dev,
    license='MIT',
    zip_safe=False,
    cmdclass={'test': PyTest},
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
)
