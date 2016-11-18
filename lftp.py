from subprocess import run, PIPE
from time import sleep


def get_files(server):
    lftp_process = run(["lftp", "-e", "cls -1; exit", "http://mirror.js-webcoding.de/pub/archlinux/core/os/x86_64/"], stdout=PIPE)
    return lftp_process.stdout.decode().split("\n")

