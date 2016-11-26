import requests
from time import time

def download_package(url):
    download = requests.get(url, stream=True)
    with open("temp/{0}".format(url.split("/")[-1]), 'wb') as f:
        ti = 0
        yield ti
        for chunk in download.iter_content(chunk_size=1024):
            if chunk:
                ti += 1
                if ti % 100 == 0:
                    yield ti
                f.write(chunk)
        yield ti


if __name__ == "__main__":
    import files
    for package in files.f:
        print(package)
        for e in download_package(package):
            print(e, end="")
        print()
