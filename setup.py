import os

import pkg_resources
from setuptools import find_packages, setup

from rekono import VERSION

current_directory = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(current_directory, 'README.md'), 'r') as readme:
    long_description = readme.read()

with open(os.path.join(current_directory, 'requirements.txt'), 'r') as requirements:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(requirements)]

setup(
    name='rekono-cli',
    packages=find_packages(),
    version=VERSION,
    description='CLI to manage Rekono',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Pablo Santiago López',
    url='https://github.com/pablosnt/rekono-cli',
    keywords=['automation', 'pentesting', 'security', 'cli', 'rekono'],
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.7',
    entry_points='''
        [console_scripts]
        rekono=rekono.main:rekono
    ''',
    project_urls={
        'Rekono': 'https://github.com/pablosnt/rekono',
        'Rekono CLI': 'https://github.com/pablosnt/rekono-cli',
    }
)
