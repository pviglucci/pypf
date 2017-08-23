"""Setup file to work with pypi and pip."""
from setuptools import setup


with open('LICENSE.txt') as f:
    license = f.read()

with open('README.rst') as f:
    long_description = f.read()


setup(name='pypf',
      version='0.9.3',
      description='Create point and figure charts',
      long_description=long_description,
      classifiers=[
                  'Development Status :: 4 - Beta',
                  'License :: OSI Approved :: MIT License',
                  'Programming Language :: Python :: 3.6',
                  'Topic :: Office/Business :: Financial :: Investment',
      ],
      keywords='point figure stock chart',
      url='http://github.com/pviglucci/pypf',
      author='Peter Viglucci',
      author_email='pviglucci@gmail.com',
      license='MIT License',
      packages=['pypf'],
      install_requires=['requests', ],
      scripts=['pf.py'],
      include_package_data=True,
      zip_safe=False)
