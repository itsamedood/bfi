from os.path import exists
from sys import exit


class Flags:
  no_chr_limit = False
  no_stdout = False
  help = False
  dump: str | None = None
  out: str | None = None

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
          case "help": self.help = True
          case f:
            print("Unknown flag: %s" %f)
            exit(1)
