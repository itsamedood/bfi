from flags import *
from interpreter import Interpreter
from io import StringIO
from os.path import exists
from sys import argv


def shell(_interpreter: Interpreter) -> None:
  lines: list[str] = []
  print("Brainfuck Interpreter (bfi) Shell", "\nType `exit` to exit the shell.")

  try:
    while True:
      code = input("%s ~ " %len(lines))
      if code == "exit": break

      data, pointer = _interpreter.parse_code(code)
      print(f"pointer = {pointer}\ndata = {data}")
      lines.append(code)

  except KeyboardInterrupt: print('\n')



  print("Exited.")


def read(_file: str, _interpreter: Interpreter) -> None:
  if not exists(_file):
    print("Could not find %s." %_file)
    exit(1)

  with open(_file, 'r') as src: _interpreter.parse_code(src.read())


if __name__ == "__main__":
  flags = Flags([f[2:] for f in argv if f[:2] == "--"])
  interpreter = Interpreter(flags)

  if len(argv) <= 1 or len([a for a in argv[1:] if not a[:2] == "--"]) < 1: shell(interpreter)
  else:
    file = argv[-1]
    read(file, interpreter)

  if flags.out is not None: interpreter.output(flags.out)
  if flags.dump is not None: interpreter.dump(flags.dump)
