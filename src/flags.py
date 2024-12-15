from enum import Enum
from sys import exit


class CharAction(Enum):
  FORWARD     = '>'
  BACKWARD    = '<'
  INCREMENT   = '+'
  DECREMENT   = '-'
  PRINT       = '.'
  INPUT       = ','
  LOOP_START  = '['
  LOOP_END    = ']'


class Flags:
  """ Represents every flag recognized by the interpreter. """

  debug = False
  no_chr_limit = False
  no_exit = False
  no_stdout = False
  no_strict_input = False
  ttc = False
  help = False
  verbose = False
  dump: str | None = None
  find: str | int | None
  format: str | None = None
  max_len: int | None = None
  max_size: int | None = None
  out: str | None = None
  bfcharset: dict[CharAction, str] = {
    CharAction.FORWARD: '>',
    CharAction.BACKWARD: '<',
    CharAction.INCREMENT: '+',
    CharAction.DECREMENT: '-',
    CharAction.PRINT: '.',
    CharAction.INPUT: ',',
    CharAction.LOOP_START: '[',
    CharAction.LOOP_END: ']'
    }

  helpmsg = """Brainfuck Interpreter (bfi)
Usage: bfi --[flags] [file]
Flags:
  --debug               | Tells you what characters are being emitted by the Brainfuck code.
  --no_chr_limit        | Removes limit of 127 when using `chr` (end of ASCII table).
  --no_exit             | Forces the interpreter to continue after an error (like a value out of range).
  --no_stdout           | Disable printing the value when using `.`.
  --no_strict_input     | Allows more than numbers acceptable with `,` (anything NaN will be converted using `ord`).
  --ttc                 | Text To Code, converts regular text to Brainfuck code.
  --help                | Shows this help menu.
  --verbose             | Show some extra info.
  --dump=<path>         | Dump the data (memory, if you will) into the specified file.
  --find=<char|int>     | Find a specific character by it's value or number and highlight it.
  --format=<bfFile>     | Formats a `.bf` file, which involves removing all characters that are not part of Brainfuck.
  --max_len=<len>       | *WORKS WITH --format* Determines length of a line till a `\\n` is appended. `0` means no `\\n`s. Default is `50`.
  --max_size=<size>     | Limits the size of the array to specified size.
  --out=<path>          | Dump the output into a file. The output is comprised of every time you print a value using `.`.
  --charset=<chars>     | Lets you change the character set from what BrainFuck normally uses, formatted as so: ><+-.,[]
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

          case "find":
            if len(value) < 1:
              print("Expected value for flag 'find'.")
              exit(1)

            self.find = int(value) if value.isnumeric() else value

          case "format":
            if len(value) < 1:
              print("Expected value for flag 'format'.")
              exit(1)

            self.format = value

          case "max_len":
            if not value.isnumeric():
              print("Value for flag 'max_len' should be an integer.")
              exit(1)

            ml = int(value)
            if ml < 0:
              print("Value for flag 'max_len' should be greater than or equal to 0.")
              exit(1)

            self.max_len = int(value)

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

          case "charset":
            if len(value) < 1:
              print("Expected value for flag 'charset'.")
              exit(1)

            elif not len(value) == 8:
              print("Flag 'charset' must be 8 characters.")
              exit(1)

            for i, key in enumerate(self.bfcharset): self.bfcharset[key] = value[i]

          case f:
            print("Unknown flag: %s" %f)
            exit(1)

      else:
        # Flags that don't need a value.
        match f:
          case "debug": self.debug = True
          case "no_chr_limit": self.no_chr_limit = True
          case "no_exit": self.no_exit = True
          case "no_stdout": self.no_stdout = True
          case "no_strict_input": self.no_strict_input = True
          case "ttc": self.ttc = True
          case "help":
            print(self.helpmsg)
            exit(0)

          case "verbose": self.verbose = True

          case f:
            print("Unknown flag: %s" %f)
            exit(1)
