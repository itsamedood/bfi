from interpreter import Interpreter
from os import system


class Shell:
  lines: list[str] = []
  data: list[int] = []
  pointer = 0
  print_d_and_p = True

  def __init__(self, _interpreter: Interpreter) -> None:
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

          self.lines.append(code if '+' in code or '-' in code or '<' in code or '>' in code or '.' in code or ',' in code or '[' in code or ']' in code else '')
          self.lines = [l for l in self.lines if len(l) > 0]

    except KeyboardInterrupt: print('\n')

    print("Exited.")

  def iscommand(self, _code: str) -> bool:
    match _code:
      case "clear": system("clear")
      case "dump": print(f"pointer = {self.pointer}\ndata = {self.data}")

      case "list":
        for i, l in enumerate(self.lines): print(f"{i+1}) {l}")

      case "help": print("""
clear | Clear the screen.
dump  | Show the pointer and data.
exit  | Exit shell.
help  | Display this menu.
list  | List all lines of code.
""")
      case _: return False

    return True
