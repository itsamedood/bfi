from flags import *
from colorama import init as init_colorama
from interpreter import Interpreter
from os.path import exists
from shell import Shell
from sys import argv


def read_bf_file(_file: str, _interpreter: Interpreter) -> None:
  if not exists(_file):
    print("Could not find %s." %_file)
    exit(1)

  with open(_file, 'r', encoding="utf-8") as src:
    if _interpreter.flags.ttc: print(_interpreter.ttc(src.read()))
    else: _interpreter.parse_code(src.read())


if __name__ == "__main__":
  init_colorama()  # Initialize colorama.

  flags = Flags([f[2:] for f in argv if f[:2] == "--"])
  interpreter = Interpreter(flags)

  if flags.format is not None: interpreter.format(flags.format)  # Placed here to not trigger the shell.

  if len(argv) <= 1 or len([a for a in argv[1:] if not a[:2] == "--"]) < 1: Shell(interpreter)
  else:
    file = argv[-1]
    read_bf_file(file, interpreter)

  if flags.dump is not None: interpreter.dump(flags.dump)
  if flags.out is not None: interpreter.output(flags.out)
