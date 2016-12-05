import click
from fpd import check, thread
from fpd.download import create_progress_bar


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

    for num, p in enumerate(packages):
        print("\rGetting package sizes ({0}/{1})".format(num+1, len(packages)), end="")
        p.update_size(mirrors[0])
    print("\r")

    print("Matching package with mirror")
    packages = check.match_packages(packages, mirrors)

    print("Downloading")
    downloader = thread.DownloadManager(packages)
    for done in downloader.start():
        print("\r" + create_progress_bar(done), end="")
    print()


if __name__ == "__main__":
    run()
