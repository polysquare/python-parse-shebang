# /setup.py
#
# Installation and setup script for parse-shebang
#
# See /LICENCE.md for Copyright information
"""Installation and setup script for parse-shebang."""

from setuptools import find_packages, setup

setup(name="parse-shebang",
      version="0.0.20",
      description="""Parse shebangs and return their components.""",
      long_description_markdown_filename="README.md",
      author="Sam Spilsbury",
      author_email="smspillaz@gmail.com",
      classifiers=["Development Status :: 3 - Alpha",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.1",
                   "Programming Language :: Python :: 3.2",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Intended Audience :: Developers",
                   "Topic :: System :: Shells",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: MIT License"],
      url="http://github.com/polysquare/python-parse-shebang",
      license="MIT",
      keywords="development",
      packages=find_packages(exclude=["test"]),
      install_requires=["six"],
      extras_require={
          "upload": ["setuptools-markdown"]
      },
      test_suite="nose.collector",
      zip_safe=True,
      include_package_data=True)
