#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages

dirname = os.path.dirname(__file__)
version = open(os.path.join(dirname, "VERSION")).read().strip()

setup(
	name="commandparse",
	version=version,
	author="flgy",
	author_email="florian.guilbert@synacktiv.com",
	keywords="CLI,command,argparse,parser",
	url="https://github.com/flgy/commandparse",
	license="MIT",
	description="CLI application commands parser",
	long_description=codecs.open("README.md", "rb", "utf8").read(),

	classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Information Technology",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python",
		"Topic :: Software Development :: Libraries",
		"Topic :: Utilities",
		"Operating System :: OS Independent",
	],

	# Packages and dependencies
	packages=find_packages(include=["commandparse"]),

	# Other configurations
	zip_safe=True,
	platforms='any',
)
