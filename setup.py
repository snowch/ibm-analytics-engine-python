from setuptools import setup, find_packages


setup(
  name='ibm-analytics-engine-python',
  version='0.0.12',
  description="IBM Analytics Engine library",
  author='Chris Snow',
  author_email='chsnow123@gmail.com',
  url='https://github.com/snowch/ibm-analytics-engine-python',
  download_url = 'https://github.com/snowch/ibm-analytics-engine-python/archive/0.0.12.tar.gz',
  packages = find_packages(exclude=["docs/example_scripts", "docs/example", "tests"]),
  keywords = 'IBM Analytics Engine Spark Hadoop',
  install_requires=[ 'requests' ],
  test_suite='nose.collector',
  tests_require=['nose'],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
  ],
)
