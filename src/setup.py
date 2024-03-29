import os

import pkg_resources
from setuptools import find_packages, setup

from rekono import VERSION

current_directory = os.path.dirname(os.path.realpath(__file__))

long_description = ''
for readme_path in [
    os.path.join(current_directory, 'README.md'),
    os.path.join(current_directory, '..', 'README.md'),
]:
    if os.path.isfile(readme_path):
        with open(readme_path, 'r') as readme:
            long_description = readme.read()
        break

with open(os.path.join(current_directory, 'requirements.txt'), 'r') as requirements:
    install_requires = [str(req) for req in pkg_resources.parse_requirements(requirements)]

setup(
    name='rekono-cli',
    packages=find_packages(exclude=['tests']),
    version=VERSION,
    description='CLI to make requests to Rekono API',
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
        rekono-cli=rekono.main:rekono
    ''',
    project_urls={
        'Rekono': 'https://github.com/pablosnt/rekono',
        'Rekono CLI': 'https://github.com/pablosnt/rekono-cli',
    }
)
