from setuptools import setup
import sys

with open("README.md", "r") as f:
  long_description = f.read()

with open("VERSION", "r") as f:
  version = f.read()

setup(
  name='Hurricane',
  version=version,
  description='A text based game',
  long_description=long_description,
  url='https://github.com/MaceroniMan/Hurricane',
  author='MaceroniMan',
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
  install_requires=[],
  packages=["hurricane", "hurricane.data", "hurricane.scripts"],
  package_data={'hurricane': ['data/assets.dat']},
  options={"bdist_wheel": {"python_tag": "py38"}},
  platforms=['any'],
)