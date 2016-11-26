from subprocess import run, PIPE
from urllib.parse import urlparse
import requests


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


def get_raw_mirrors():
    return requests.get("https://www.archlinux.org/mirrors/status/json/").json()["urls"]

def get_mirrors():
    return sorted([(mirror["url"], mirror["score"]) for mirror in get_raw_mirrors() if mirror["score"] and mirror["url"]], key=lambda e: e[1])
