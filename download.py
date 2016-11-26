import requests
from time import time

def download_package(url):
    download = requests.get(url, stream=True)
    with open("temp/{0}".format(url.split("/")[-1]), 'wb') as f:
        ti = 0
        yield "\r{0}KB".format(ti)
        for chunk in download.iter_content(chunk_size=1024):
            if chunk:
                ti += 1
                if ti % 50 == 0:
                    yield "\r{0}KB".format(ti)
                f.write(chunk)
        yield "\r{0}".format(ti)


if __name__ == "__main__":
    import files
    for package in files.f:
        print(package)
        for e in download_package(package):
            print(e, end="")
        print()
