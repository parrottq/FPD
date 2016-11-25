from subprocess import run, Popen, PIPE
from urllib.parse import urlparse
from time import sleep


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


def download_package(link, directory="temp/"):
    process = Popen(["lftp", "-c", "mget", "-O", directory, link])
    while process.poll() == None:
        sleep(0.1)

# Unavailable
if __name__ == "__main__" and False:
    packages = get_updates()
    num_packages = len(packages)
    for package_count, package in enumerate(packages):
        print("\x1b[32mDownload: {0} \x1b[33m({1}/{2})\x1b[0m".format(package[package.rfind('/')+1:package.rfind('-')], package_count+1, num_packages))
        download_package(package)
