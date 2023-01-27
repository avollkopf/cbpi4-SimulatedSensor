from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='cbpi4-SimulatedSensor',
      version='0.0.3',
      description='This plugin allowes you to simulate a sensor. The sensor will check if a Kettle is currently heating and will increase its value by a configurable amount. If the Kettle is not heating the temperature will be decreased by a configurable amount.',
      author='prash3r',
      author_email='pypi@prash3r.de',
      url='https://pypi.org/project/cbpi4-SimulatedSensor/',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4_SimulatedSensor': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4_SimulatedSensor'],
      long_description=long_description,
      long_description_content_type='text/markdown'
     )
