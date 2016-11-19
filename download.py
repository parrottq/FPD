from subprocess import run, PIPE
from urllib.parse import urlparse


def is_link(link):
    try:
        p = urlparse(link)
        if p.scheme in ["rsync", "https", "http"]:
            return True
    except OSError:
        pass
    return False


def get_updates():
    mirrors = run(["pacman", "-Spu"], stdout=PIPE).stdout.decode().split('\n')
    
    for mirror in mirrors:
        if not is_link(mirror):
            mirrors.remove(mirror)

    return mirrors


def download_package(package):
    pass
