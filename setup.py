from setuptools import setup, find_packages


setup(
  name='ibm-analytics-engine-python',
  version='0.0.1',
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/snowch/ibm-analytics-engine-python',
  packages = find_packages(exclude=["docs/example", "tests"]),
  install_requires=[ 'requests' ],
  test_suite='nose.collector',
  tests_require=['nose'],
)
