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


def to_rel_url(url):
    return "/".join(url.split("/")[-4:])


def get_updates():
    mirrors = [mirror for mirror in run(["pacman", "-Syup"], stdout=PIPE).stdout.decode().split('\n') if is_link(mirror)]
    return [to_rel_url(mirror) for mirror in mirrors]


def get_dependecies(package):
    mirrors = [mirror for mirror in run(["pacman", "-Sp", package], stdout=PIPE).stdout.decode().split('\n') if is_link(mirror)]
    return [to_rel_url(mirror) for mirror in mirrors]


def get_raw_mirrors():
    return requests.get("https://www.archlinux.org/mirrors/status/json/").json()["urls"]


def get_mirrors():
    mirrors = sorted([(mirror["url"], mirror["score"]) for mirror in get_raw_mirrors() if mirror["score"] and mirror["url"]], key=lambda e: e[1])
    return [mirror[0] for mirror in mirrors]


def get_package_size(packages, mirror):
    return [(package, int(requests.head(combine_url(mirror, package)).headers["Content-Length"])) for package in packages]


def combine_url(base, url):
    return base + "/".join(url.split("/")[-4:])


def match_packages(packages, mirrors, cap=100*1000):
    url_packages = []
    mirrors = [list(mirror) for mirror in zip(mirrors, [cap]*len(mirrors))]

    # Deal with packages that are bigger than data cap
    for package in packages:
        if package[1] > cap:
            url_packages.append((mirrors.pop(0)[0], package[0]))

    # Assign packages to mirrors while enforcing data caps for each mirror
    for package in packages:
        for mirror in mirrors:
            if mirror[1] - package[1] > 0:
                mirror[1] = mirror[1] - package[1]
                url_packages.append((mirror[0], package[0]))
                break
    return url_packages

if __name__ == "__main__":
    import files
    mirrors = get_mirrors()
    for package in match_packages(get_package_size(get_updates(), mirrors[0]), mirrors):
        print(package[0], package[1])
