import requests
from time import time
from shutil import get_terminal_size
from math import ceil
from os.path import isdir
from os import mkdir


colours = {
        "reset"  : "\x1b[0m",
        "green"  : "\x1b[32m",
        "yellow" : "\x1b[33m",
}


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


def create_progress_bar(progress):
    t_size = get_terminal_size().columns

    start ="["
    end = "] {0}{1}KB/{2}KB".format(" " * (len(str(progress[2])) - len(str(progress[0]+progress[1]))), int((progress[0]+progress[1])/1000), int(progress[2]/1000))
    len_bar = t_size - len(start+end)
    conversion = len_bar / progress[2]


    body = []
    body.append("".join(["#" for e in range(int(progress[1] * conversion))]))
    body.append("".join(["#" for e in range(int(progress[0] * conversion))]))
    body.append("".join(["-" for e in range(len_bar - len("".join(body)))]))

    body_colour = [
        colours["green"], # Colour of finished package sizes
        colours["yellow"], # Colour of unfinished package sizes
        colours["reset"], # Resets colour
    ]
    progress = ""
    for b in zip(body_colour, body):
        progress += "".join(b)

    return start + progress + end


if __name__ == "__main__":
    for package in files.f:
        print(package)
        for e in download_package(package):
            print(e, end="")
        print()
