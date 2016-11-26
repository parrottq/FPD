import threading
from download import download_package
import check
from time import sleep


class Downloader(threading.Thread):
    def __init__(self, url, size):
        super().__init__()
        self.url = url
        self.name = ".".join(url.split("/")[-1].split(".")[:-3])
        self.size = size
        self.progress = 0

    def run(self):
        for progress in download_package(self.url):
            self.progress = progress
        self.progress = self.size


class DownloadManager:
    def __init__(self, packages, max_threads=4):
        self.threads = [Downloader(url, size) for url, size in packages]
        self.nthreads = len(self.threads)
        self.running = []
        self.nrunning = 0
        self.packages = packages
        self.max = max_threads

        size = 0
        for s in self.threads:
            size += s.size
        self.total_size = size
        self.done_size = 0
        self.removed_size = 0


    def start(self):
        while self.nthreads or self.nrunning:
            for thread in self.running:
                if not thread.is_alive():
                    thread.join()
                    self.removed_size += thread.size
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
                self.done_size += t.progress * 1000
            self.done_size += self.removed_size

            yield (self.done_size, self.total_size)
            sleep(0.1)
        print()


if __name__ =="__main__":
    import files
    mirrors = check.get_mirrors()
    packages = check.match_packages(check.get_package_size(files.f, mirrors[0]), mirrors)

    dm = DownloadManager(packages)
    for done in dm.start():
        print(done)

