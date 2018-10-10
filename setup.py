#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

# I used the following resources to compile the packaging boilerplate:
# https://python-packaging.readthedocs.io/en/latest/
# https://packaging.python.org/distributing/#requirements-for-packaging-and-distributing

from setuptools import find_packages, setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='search_engine',
      version='0.1.0',
      description='User inteface for Whoosh',
      long_description=readme(),
      url='https://github.com/DavidNemeskey/search_engine',
      author='Dávid Márk Nemeskey',
      license='MIT',
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 1 - Proof of Concept',

          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Topic :: Internet :: WWW/HTTP :: Indexing/Search'

          # Environment
          'Operating System :: POSIX :: Linux',
          'Environment :: Console',
          'Natural Language :: English',

          # Pick your license as you wish (should match "license" above)
           'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      keywords='indexing search information retrieval',
      packages=find_packages(exclude=['scripts']),
      # Include the configuration -- unfortunately, MANIFEST.in doesn't seem
      # to do it for bdist (and package_data for sdist)
      package_data={
          'conf': ['*'],
      },
      # Install the scripts
      scripts=[
          'scripts/index.py',
          # 'scripts/search.py',
      ],
      # Tensorflow and numpy can be installed from requirement files, as they
      # are only required if the nn module / scripts are used.
      install_requires=[
          'whoosh'
      ],
      # zip_safe=False,
      use_2to3=False)
