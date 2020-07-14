"""
Copyright 2019 Cognitive Scale, Inc. All Rights Reserved.

See LICENSE.txt for details.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import find_packages
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

__version__ = '1.3.3'

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
        'numpy==1.18.4',
        'scikit-learn==0.23.1',
        'pandas==0.24.2',
        'Flask==1.1.1',
        'cortex-python==1.3.1',
        'keras==2.3.1',
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
