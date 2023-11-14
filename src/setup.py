import os
from pathlib import Path

import pkg_resources
from setuptools import find_packages, setup

from rekono import VERSION

current_directory = Path(__file__).resolve()

long_description = ""
for readme in [
    current_directory / "README.md",
    current_directory.parent / "README.md",
]:
    if readme.is_file():
        long_description = readme.read_text(encoding="utf-8")
        break

with (current_directory / "requirements.txt").open() as requirements:
    install_requires = [
        str(req) for req in pkg_resources.parse_requirements(requirements)
    ]

setup(
    name="rekono-cli",
    packages=find_packages(exclude=["tests"]),
    version=VERSION,
    description="CLI to make requests to Rekono API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pablo Santiago López",
    url="https://github.com/pablosnt/rekono-cli",
    keywords=["automation", "pentesting", "security", "cli", "rekono"],
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.7",
    entry_points="""
        [console_scripts]
        rekono-cli=rekono.main:rekono
    """,
    project_urls={
        "Rekono": "https://github.com/pablosnt/rekono",
        "Rekono CLI": "https://github.com/pablosnt/rekono-cli",
    },
)
