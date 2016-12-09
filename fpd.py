#! /usr/bin/python
import click
from fpd import check, thread
from fpd.download import create_progress_bar
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

    sizes = thread.SizeManager(packages, thread_max=16)
    for done, total in sizes.start():
        print("\rGetting sizes ({0}/{1})".format(done, total), end="")
    print()
    packages = [t.package for t in sizes.threads]

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
