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

            yield ((self.done_size, self.removed_size, self.all_size), [int(thread.progress/thread.package.size * 100) for thread in self.running])
            sleep(0.1)
        print()


class Sizer(threading.Thread):
    def __init__(self, package):
        super().__init__()
        self.package = package
        self.done = 0

    def run(self):
        self.done = 1
        self.package.update_size()
        self.done = 2


class SizeManager:
    def __init__(self, packages, thread_max=8):
        self.packages = packages
        self.threads = [Sizer(package) for package in packages]
        self.max = thread_max
        self.active = 0
        self.done_count = 0

    def start(self):
        done = False
        yield (self.done_count, len(self.threads))
        while not done:
            for thread in self.threads:
                if self.active < self.max and thread.done == 0:
                    self.active += 1
                    thread.start()

                if thread.done == 2:
                    thread.done = 3
                    self.active -= 1
                    self.done_count += 1
                    yield (self.done_count, len(self.threads))
                    if self.done_count == len(self.threads):
                        done = True

            sleep(0.1)


if __name__ =="__main__":
    print("\rFetching mirrors...", end="")
    mirrors = check.get_mirrors()
    print("\rMatching package with mirror...", end="")
    packages = check.match_packages(check.get_package_size(check.get_updates(), mirrors[0]), mirrors)

    dm = DownloadManager(packages)
    for done in dm.start():
        print("\r" + create_progress_bar(done), end="")
    print()

