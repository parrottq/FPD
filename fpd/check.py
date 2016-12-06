from subprocess import run, PIPE
from urllib.parse import urlparse
import requests


class Package:
    def __init__(self, url):
        self.rel_url = self._to_rel(url)
        self.base_url = url
        self.size = -1

    def update_size(self):
        self.size = int(requests.head(self.base_url).headers["Content-Length"])

    def update_base_url(self, url):
        self.base_url = self._to_base(url)

    def _to_rel(self, url): # make none private
        return "/".join(url.split("/")[-4:])

    def _to_base(self, base):
        return base + "/".join(self.rel_url.split("/")[-4:])


def is_link(link):
    try:
        p = urlparse(link)
        if p.scheme in ["https", "http"]:
            return True
    except OSError:
        pass
    return False


def get_updates():
    return [mirror for mirror in run(["pacman", "-Syup"], stdout=PIPE).stdout.decode().split('\n') if is_link(mirror)]


def get_dependencies(package):
    return [mirror for mirror in run(["pacman", "-Sp", package], stdout=PIPE).stdout.decode().split('\n') if is_link(mirror)]


def get_raw_mirrors():
    return requests.get("https://www.archlinux.org/mirrors/status/json/").json()["urls"]


def get_mirrors():
    mirrors = sorted([(mirror["url"], mirror["score"]) for mirror in get_raw_mirrors() if mirror["score"] and mirror["url"]], key=lambda e: e[1])
    return [mirror[0] for mirror in mirrors if is_link(mirror[0])]


def match_packages(packages, mirrors, cap=100*1000):
    url_packages = []
    mirrors = [list(mirror) for mirror in zip(mirrors, [cap]*len(mirrors))]

    # Deal with packages that are bigger than data cap
    for package in packages:
        if package.size > cap:
            mirror = mirrors.pop(0)[0]
            package.update_base_url(mirror)
            url_packages.append(package)

    # Assign packages to mirrors while enforcing data caps for each mirror
    for package in packages:
        for mirror in mirrors:
            if mirror[1] - package.size > 0:
                mirror[1] = mirror[1] - package.size
                package.update_base_url(mirror[0])
                url_packages.append(package)
                break
    return url_packages

if __name__ == "__main__":
    print("Fetching mirrors")
    mirrors = get_mirrors()
    packages = [Package(url) for url in get_updates()]

    print("Getting sizes")
    for package in packages:
        package.update_size(mirrors[0])

    print("Matching packages with mirrors")
    for e in match_packages(packages, mirrors):
        print(e.base_url)
