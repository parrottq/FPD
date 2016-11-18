from subprocess import run, PIPE


def parse_update(update):
    update = update.split(" ")
    if len(update) == 4:
        update.remove("->")
        return dict(zip(["package", "old", "new"], update))
    else:
        return False


def get_updates():
    updates = run(["checkupdates"], stdout=PIPE)
    lupdates = list(filter(None, updates.stdout.decode().split('\n')))
    decoded = []
    for update in lupdates:
        data = parse_update(update)
        if data:
            yield data

