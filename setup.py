from setuptools import setup
import os
import sys

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    if sys.version_info < (3,3):
        requires = ['mock']  # for python2 and python < 3.3
    else:
        requires = []  # for >= python3.3

else:
    # Place install_requires into the text file "requirements.txt"
    with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f2:
        requires = f2.read().strip().splitlines()

setup(name='computer',
      version='0.1',
      description='Abstraction for performing tasks on servers.',
      url='http://github.com/jrising/computer',
      author='James Rising',
      author_email='jarising@gmail.com',
      license='GNU v. 3',
      packages=['computer'],
      zip_safe=False)
