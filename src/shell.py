from interpreter import Interpreter
from os import system


class Shell:
  """ Manages the interpreter in shell mode. """

  lines: list[str] = []
  print_d_and_p = True

  def __init__(self, _interpreter: Interpreter) -> None:
    self.interpreter = _interpreter

    print("Brainfuck Interpreter (bfi) Shell", "\nType `help` for a list of commands, or `exit` to exit the shell.")

    try:
      while True:
        code = input("%s ~ " %len(self.lines))

        if code == "exit": break
        if self.iscommand(code): self.print_d_and_p = False

        if _interpreter.flags.ttc:
          transcode = _interpreter.ttc(code)
          print(transcode)

        else:
          self.data, self.pointer = _interpreter.parse_code(code)
          if self.print_d_and_p: print(f"pointer = {self.pointer}\ndata = {self.data}")
          else: self.print_d_and_p = True

          # Allows comments to count as lines.
          if not self.iscommand(code, True) and len(code) > 0: self.lines.append(code)
          # self.lines = [l for l in self.lines if len(l) > 0]

    except KeyboardInterrupt: print('\n')
    print("Exited.")

  def iscommand(self, _code: str, _onlycheck = False) -> bool:
    match _code:
      case "clear":
        if not _onlycheck: system("clear")
      case "dump":
        if not _onlycheck: print(f"pointer = {self.pointer}\ndata = {self.data}")
      case "list":
        if not _onlycheck: [print(f"{i+1}) {l}") for i, l in enumerate(self.lines)]

      case "help":
        if not _onlycheck: print("""
clear | Clear the screen.
dump  | Show the pointer and data.
exit  | Exit shell.
help  | Display this menu.
list  | List all lines of code.
reset | Wipe all lines, the data array, and set the pointer back to `0`.
""")

      case "reset":
        if not _onlycheck:
          self.lines = []
          self.interpreter.pointer = 0
          self.interpreter.data = [0]

      case _: return False

    return True
