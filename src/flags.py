from sys import exit


class Flags:
  no_chr_limit = False
  no_exit = False
  no_stdout = False
  ttc = False
  help = False
  dump: str | None = None
  max_size: int | None = None
  out: str | None = None

  helpmsg = """Brainfuck Interpreter (bfi)
Usage: bfi --[flags] [file]
Flags:
  --no_chr_limit    | Removes limit of 127 when using `chr` (end of ASCII table).
  --no_exit         | Forces the interpreter to continue after an error (like a value out of range).
  --no_stdout       | Disable printing the value when using `.`.
  --ttc             | Text To Code, converts regular text to Brainfuck code.
  --help            | Shows this help menu.
  --dump=<path>     | Dump the data (memory, if you will) into the specified file.
  --max_size=<size> | Limits the size of the array to specified size.
  --out=<path>      | Dump the output into a file. The output is comprised of every time you print a value using `.`.
"""

  def __init__(self, _flags: list[str]) -> None:
    for f in _flags:
      # Flags that need a value.
      if '=' in f:
        s = f.split('=')
        name, value = s[0], s[1]

        match name:
          case "dump":
            if len(value) < 1:
              print("Expected value for flag 'dump'.")
              exit(1)

            self.dump = value

          case "max_size":
            if not value.isnumeric():
              print("Value for flag 'max_size' should be an integer.")
              exit(1)

            ms = int(value)
            if ms <= 0:
              print("Value for flag 'max_size' should be greater than 0.")
              exit(1)

            self.max_size = int(value)

          case "out":
            if len(value) < 1:
              print("Expected value for flag 'dump'.")
              exit(1)

            self.out = value

          case f:
            print("Unknown flag: %s" %f)
            exit(1)

      else:
        # Flags that don't need a value.
        match f:
          case "no_chr_limit": self.no_chr_limit = True
          case "no_exit": self.no_exit = True
          case "no_stdout": self.no_stdout = True
          case "ttc": self.ttc = True
          case "help":
            print(self.helpmsg)
            exit(0)

          case f:
            print("Unknown flag: %s" %f)
            exit(1)
