"""Setup file to work with pypi and pip."""
from setuptools import setup


def _license():
    try:
        with open('LICENSE.txt') as f:
            return f.read()
    except Exception:
        return ''


def _readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except Exception:
        return ''


setup(name='pypf',
      version='0.9',
      description='Create point and figure charts',
      long_description=_readme(),
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
      license=_license(),
      packages=['pypf'],
      install_requires=['requests', ],
      scripts=['pf.py'],
      include_package_data=True,
      zip_safe=False)
