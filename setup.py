from setuptools import setup

setup(
  name='Hurricane',
  version='0.1.0',
  description='A text based game',
  url='https://github.com/MaceroniMan/Hurricane',
  author='MaceroniMan',
  classifiers=[
    'Programming Language :: Python :: 3.8',
  ],
  install_requires=[],
  packages=["hurricane", "hurricane.data"],
  package_data={'hurricane': ['data/assets.dat']},
  options={"bdist_wheel": {"python_tag": "py38"}},
)