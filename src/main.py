from flags import *
from io import StringIO
from sys import argv


class Interpreter:
  def __init__(self, _flags: Flags) -> None:
    self.data = [0]
    self.pointer = 0
    self.output = StringIO()
    self.flags = _flags

  def parse_code(self, _code: str) -> tuple[list[int], int]:
    i, loopstart = 0, 0

    while i < len(_code):
      c = _code[i]

      match c:
        case '>':
          self.pointer += 1
          if len(self.data) < self.pointer + 1: self.data.append(0)

        case '<':
          if self.pointer > 0: self.pointer -= 1

        case '+': self.data[self.pointer] += 1

        case '-': self.data[self.pointer] -= 1

        case '.':
          value = self.data[self.pointer]

          if value < 0 or (not self.flags.no_chr_limit and value > 127): print("%s out of range." %value)
          else:
            char = chr(self.data[self.pointer])
            self.output.write(char)
            if not self.flags.no_stdout: print(char)

        case ',':
          uinput: int | None = None
          while uinput is None:
            try:
              uinput = int(input("Input: "))
            except: uinput = None

          self.data[self.pointer] = uinput

        case '[':
          if ']' not in _code:
            print("Loop never closed.")
            break

          else: loopstart = i

        case ']':
          if self.data[self.pointer] == 0: loopstart = 0
          else: i = loopstart

      i += 1

    return (self.data, self.pointer)


def shell(_flags: Flags) -> None:
  interp = Interpreter(_flags)
  lines: list[str] = []
  print("Brainfuck Interpreter (bfi)")

  try:
    while True:
      code = input("%s ~ " %len(lines))
      data, pointer = interp.parse_code(code)

      print(f"pointer = {pointer}\ndata = {data}")
      lines.append(code)

  except KeyboardInterrupt:
    print('\n')

    if _flags.out is not None:
      print("Output: %s" %interp.output.getvalue())
    print("Exited.")


def read(_file: str, _flags: Flags) -> None:
  if not exists(_file):
    print("Could not find %s." %_file)
    exit(1)

  with open(_file, 'r') as src: Interpreter(_flags).parse_code(src.read())


if __name__ == "__main__":
  flags = Flags([f[2:] for f in argv if f[:2] == "--"])

  if flags.help:
    print("""Brainfuck Interpreter (bfi)
Usage: bfi [flags] [file]
Flags:
  --no_chr_limit | Removes limit of 127 when using `chr` (end of ASCII table).
  --no_stdout   | Disable printing the value when using `.`.
  --help         | Shows this help menu.
  --dump         | Dump the data (memory, if you will) into a file.
  --out          | Dump the output into a file. The output is comprised of every time you print a value using `.`.
""")
    exit(0)

  if len(argv) <= 1 or len([a for a in argv if not a[:2] == "--"]) > 0: shell(flags)
  else:
    file = argv[-1]

    read(file, flags)
