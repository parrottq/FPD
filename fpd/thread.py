import threading
from . import download, check
from time import sleep


class Downloader(threading.Thread):
    def __init__(self, package):
        super().__init__()
        self.package = package
        self.progress = 0

    def run(self):
        for progress in download.download_package(self.package.base_url):
            self.progress = progress
        self.progress = self.package.size


class DownloadManager:
    def __init__(self, packages, max_threads=4):
        self.threads = [Downloader(package) for package in packages]
        self.nthreads = len(self.threads)
        self.running = []
        self.nrunning = 0
        self.packages = packages
        self.max = max_threads

        size = 0
        for s in self.threads:
            size += s.package.size
        self.all_size = size
        self.done_size = 0
        self.removed_size = 0


    def start(self):
        while self.nthreads or self.nrunning:
            for thread in self.running:
                if not thread.is_alive():
                    thread.join()
                    self.removed_size += thread.package.size
                    self.running.remove(thread)
                    self.nrunning = len(self.running)

            for new_thread in range(self.max - self.nrunning):
                if self.nthreads:
                    thread = self.threads.pop()
                    self.nthreads = len(self.threads)
                    thread.start()

                    self.running.append(thread)
                    self.nrunning = len(self.running)

            self.done_size = 0
            for t in self.running:
                self.done_size += t.progress

            yield (self.done_size, self.removed_size, self.all_size)
            sleep(0.1)
        print()


if __name__ =="__main__":
    print("\rFetching mirrors...", end="")
    mirrors = check.get_mirrors()
    print("\rMatching package with mirror...", end="")
    packages = check.match_packages(check.get_package_size(check.get_updates(), mirrors[0]), mirrors)

    dm = DownloadManager(packages)
    for done in dm.start():
        print("\r" + create_progress_bar(done), end="")
    print()

