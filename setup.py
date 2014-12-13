# /setup.py
#
# Installation and setup script for polysquare-cmake-linter
#
# See LICENCE.md for Copyright information

from setuptools import setup, find_packages

setup(name='polysquare-cmake-linter',
      version='0.0.1',
      description='Polysquare CMake Linter',
      long_description='Lint a CMake file for the polysquare CMake style guide',
      author='Sam Spilsbury',
      author_email='smspillaz@gmail.com',
      classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Developers',
           'Topic :: Software Development :: Build Tools',
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 3',
      ],
      license='MIT',
      keywords='development linters',
      packages=find_packages(exclude=['tests']),
      extras_require={
          'test': ['coverage']
      },
      entry_points={
          'console_scripts': [
              'polysquare-cmake-linter=polysquarecmakelinter.linter:main'
          ]
      },
      test_suite="nose.collector")
