"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://packaging.python.org/en/latest/tutorials/packaging-projects/
https://github.com/pypa/sampleproject
"""

# Python Standard Library Imports
import os
# To use a consistent encoding
from codecs import open

# Third Party (PyPI) Imports
# Always prefer setuptools over distutils
from setuptools import (
    find_packages,
    setup,
)


here = os.path.abspath(os.path.dirname(__file__))


about = {}
with open(os.path.join(here, 'htk', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)


with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name=about['__title__'],
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    # The project's main homepage.
    url=about['__url__'],
    # Author details
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: General',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
    ],
    # What does your project relate to?
    keywords='python debugging slack requests apis',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'python-dotenv>=0.13.0',
        'requests>=2',
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],  # ['check-manifest'],
        'test': [
            #'coverage',
            'pytest',
            'pytest-cov',
        ],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        #'sample': ['package_data.dat'],
    },
    package_dir={
        'htk': 'htk',
    },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [],
    },
    project_urls={
        'Documentation': about['__url__'],
        'Source': about['__url__'],
    },
)
