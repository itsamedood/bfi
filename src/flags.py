from sys import exit


class Flags:
  no_chr_limit = False
  no_stdout = False
  ttc = False
  help = False
  dump: str | None = None
  out: str | None = None

  helpmsg = """Brainfuck Interpreter (bfi)
Usage: bfi [flags] [file]
Flags:
  --no_chr_limit | Removes limit of 127 when using `chr` (end of ASCII table).
  --no_stdout    | Disable printing the value when using `.`.
  --ttc          | Text To Code, converts regular text to Brainfuck code.
  --help         | Shows this help menu.
  --dump         | Dump the data (memory, if you will) into the specified file.
  --out          | Dump the output into a file. The output is comprised of every time you print a value using `.`.
"""

  def __init__(self, _flags: list[str]) -> None:
    for f in _flags:
      if '=' in f:
        s = f.split('=')
        name, value = s[0], s[1]

        match name:
          case "dump":
            if len(value) < 1:
              print("Expected value for flag 'dump'.")
              exit(1)

            self.dump = value

          case "out":
            if len(value) < 1:
              print("Expected value for flag 'dump'.")
              exit(1)

            self.out = value

      else:
        match f:
          case "no_chr_limit": self.no_chr_limit = True
          case "no_stdout": self.no_stdout = True
          case "ttc": self.ttc = True
          case "help":
            print(self.helpmsg)
            exit(0)

          case f:
            print("Unknown flag: %s" %f)
            exit(1)
