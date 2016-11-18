from subprocess import run, PIPE


def get_arch():
    return run(["uname", "-m"], stdout=PIPE).stdout.decode().strip('\n')


def remove_comment(arg):
    if '#' in arg:
        arg = arg[:arg.find('#')]
    return arg


def parse_raw_mirror(raw_mirror):
    return raw_mirror.split(" ")[-1].strip('\n')


def get_mirrors():
    with open("/etc/pacman.d/mirrorlist") as mirror_file:
        raw_mirrors = mirror_file.readlines()

    arch = get_arch()
    
    mirrors = []
    for raw_mirror in raw_mirrors:
        if len(raw_mirror) > 0:
            mirrors.append(parse_raw_mirror(remove_comment(raw_mirror)).replace("$arch", arch))

    return list(filter(None, mirrors))


def find_package(package):
    pass


def download_package(package):
    pass
