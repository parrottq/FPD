


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
