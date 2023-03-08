"""
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

__version__ = '1.3.9'

setup(name='cortex-certifai-reference-model-server',
      description="Python Package for the CognitiveScale Cortex Certifai Reference Models",
      long_description=long_description,
      long_description_content_type='text/Markdown',
      version=__version__,
      author='CognitiveScale',
      author_email='info@cognitivescale.com',
      url='https://www.cognitivescale.com/',
      license='LICENSE',
      platforms=['linux', 'osx'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        'numpy>=1.19.5, <1.23',
        'scikit-learn>=0.20.3,<1.1',
        'pandas>=0.23.4,<1.5',
        'flask>=2.2.3',
        'markupsafe>=2.1',
        'gevent==21.12.0;platform_system!="Windows"',
        'greenlet>=1.1.0,<2.0;platform_system!="Windows"',
        'gunicorn==20.1.0;platform_system!="Windows"',
      ],


      classifiers=[
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.6',
      ],

      entry_points={
          'console_scripts': [
              'startCertifaiModelServer=certifaiReferenceModelServer.start:start_all'
              ]
      }
      )
