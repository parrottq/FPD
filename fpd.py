#! /usr/bin/python
import click
from fpd import check, thread
from fpd.download import create_progress_bar
import grequests
from shutil import get_terminal_size


@click.command()
@click.option("-P", default=None)
def run(p):
    if p:
        # Specific package
        packages = check.get_dependencies(p)
    else:
        # System update
        packages = check.get_updates()
        if not packages:
            print("No updates")
            return

    packages = [check.Package(package) for package in packages]
    install_packages(packages)


def install_packages(packages):
    print("Fetching mirrors")
    mirrors = check.get_mirrors()

    rqs = (grequests.head(package.base_url) for package in packages)
    total_packages = len(packages)
    packages = []
    for num, done in enumerate(grequests.imap(rqs, size=4)):
        print("\rGetting sizes ({0}/{1})".format(num+1, total_packages), end="")
        p = check.Package(done.url)
        p.size = int(done.headers["Content-Length"])
        packages.append(p)
    print()

    print("Matching package with mirror")
    packages = check.match_packages(packages, mirrors)

    print("Downloading")
    downloader = thread.DownloadManager(packages)
    for done, per_package in downloader.start():
        t_size = get_terminal_size().columns
        for e in range(4 - len(per_package)):
            print("\r" + " " * t_size)
        for per in per_package:
            print("\r" + create_progress_bar((per, 0, 100), int(t_size/3*2)))

        print("\r" + create_progress_bar(done, t_size), end="\x1b[1A" * 4)
    for e in range(4+1):
        print(" " * t_size)
    print("\x1b[1A" * 4 * 2)


if __name__ == "__main__":
    run()
