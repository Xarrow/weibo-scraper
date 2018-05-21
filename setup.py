import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='UTF-8') as f:
    long_description = '\n' + f.read()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    version="1.0.4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="weibo-scraper",
    url="https://github.com/Xarrow/weibo-scraper",
    author="helixcs",
    author_email="zhangjian12424@gmail.com",
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    install_requires=['requests'],
    keywords="weibo scraper crawl",
    # If your package is a single module, use this instead of 'packages':
    py_modules=['weibo_scraper'],
    # If your package has custom module ,
    # Full list :https://docs.python.org/3.6/distutils/setupscript.html
    packages=['weibo_base'],
    python_requires='>=3.6',
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
