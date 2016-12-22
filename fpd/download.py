import requests
from time import time
from shutil import get_terminal_size
from math import ceil
from os.path import isdir
from os import mkdir


def download_package(url):
    download = requests.get(url, stream=True)

    if not isdir("/var/cache/fpd"):
        mkdir("/var/cache/fpd")

    with open("/var/cache/fpd/{0}".format(url.split("/")[-1]), 'wb') as f:
        ti = 0
        yield ti
        for chunk in download.iter_content(chunk_size=1024):
            if chunk:
                ti += 1024
                yield ti
                f.write(chunk)
        yield ti


if __name__ == "__main__":
    for package in files.f:
        print(package)
        for e in download_package(package):
            print(e, end="")
        print()
