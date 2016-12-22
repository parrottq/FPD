#!/usr/bin/python

from distutils.core import setup

setup(name="FPD",
        version="1.0",
        description="Faster Pacman Downloader",
        long_description="Parallel Package Downloader for Arch Linux",
        author="Quinn Parrott",
        url="https://github.com/parrottq/FPD",
        packages=["fpd_lib"],
        scripts=["fpd"],
        )
