

colours = {
        "reset"  : "\x1b[0m",
        "green"  : "\x1b[32m",
        "yellow" : "\x1b[33m",
    }


class Multiline:
    move = {"up": "\x1b[1A", "down": "\n" } #"\x1b[1B"}

    def __init__(self):
        self.current_line = 0
        self.far = 0

    def clear_line(self, line_size):
        print("\r" + " " * line_size, end="")

    def clear_lines(self, line_size):
        print(self.move["down"] * (self.far - self.current_line), end="")
        for l in range(self.far - self.current_line):
            self.clear_line(line_size)
            print(self.move["up"], end="")

    def print(self, text, line, line_size):
        if line == self.current_line:
            self.clear_line(line_size)
            print(text, end="")

        elif line > self.current_line:
            print(self.move["down"] * (line - self.current_line), end="\r")
            print(text, end="")
            self.current_line = line
            if line > self.far:
                self.far = line

        elif line < self.current_line:
            print(self.move["up"] * (self.current_line - line), end="\r")
            print(text, end="")
            self.current_line = line


def create_progress_bar(progress, t_size):
    start ="["
    percentage = ((progress[0] + progress[1]) / progress[2]) * 100
    end = "] {0}{1}%".format(" " * (3 - len(str(int(percentage)))), int(percentage))
    len_bar = t_size - len(start+end)
    conversion = len_bar / progress[2]


    body = []
    body.append("".join(["#" for e in range(int(progress[1] * conversion))]))
    body.append("".join(["#" for e in range(int(progress[0] * conversion))]))
    body.append("".join(["-" for e in range(len_bar - len("".join(body)))]))

    body_colour = [
        colours["green"], # Colour of finished package sizes
        colours["yellow"], # Colour of unfinished package sizes
        colours["reset"], # Resets colour
    ]
    progress = ""
    for b in zip(body_colour, body):
        progress += "".join(b)

    return start + progress + end
