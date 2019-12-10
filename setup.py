#!/usr/bin/env python
from setuptools import setup, find_packages

with open("requirements/prod.txt", "r") as fh:
    requirements = fh.read().splitlines()

with open("requirements/dev.txt", "r") as fh:
    dev_requirements = fh.read().splitlines()

with open("requirements/ldap.txt", "r") as fh:
    ldap_requirements = fh.read().splitlines()

with open("requirements/social.txt", "r") as fh:
    social_requirements = fh.read().splitlines()

with open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="alcali",
    version=version,
    author="Matt Melquiond",
    author_email="matt.LLVW@gmail.com",
    description="Alcali",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/latenighttales/alcali.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
    ],
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "ldap": ldap_requirements,
        "social": social_requirements,
    },
    entry_points={"console_scripts": ["alcali = bin:manage"]},
)
