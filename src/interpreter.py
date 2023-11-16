from colorama import Fore
from flags import Flags
from io import StringIO
from os.path import exists
from sys import exit


class Interpreter:
  def __init__(self, _flags: Flags) -> None:
    self.data = [0] if _flags.max_size is None else [0 for _ in range(_flags.max_size)]
    self.pointer = 0
    self.op = StringIO()
    self.flags = _flags

  def _clear_strios(self, *strios: StringIO) -> None:
    for strio in strios:
      strio.seek(0)
      strio.truncate(0)

  def parse_code(self, _code: str) -> tuple[list[int], int]:
    i, loopstart = 0, 0

    # Use a while loop since it allows us to jump back x characters for looping.
    while i < len(_code):
      c = _code[i]

      match c:
        case '>':
          self.pointer += 1

          if len(self.data) < self.pointer + 1:
            if self.flags.max_size is not None and len(self.data) == self.flags.max_size:
              print(f"╭─ Cannot exceed max size of {self.flags.max_size}.\n╰─> {''.join([f"{Fore.RED}{l}{Fore.RESET}" if j == i else l for j, l in enumerate(_code)])}")
              self.pointer -= 1

            else: self.data.append(0)

        case '<':
          if self.pointer > 0: self.pointer -= 1

        case '+': self.data[self.pointer] += 1

        case '-': self.data[self.pointer] -= 1

        case '.':
          value = self.data[self.pointer]

          #                          >>+++++++++++++[<++++++++++>-]<.
          # >++++++++[<+++++++++>-]<.                                >>++++++++[<+++++++++>-]<.
          # The statement above produces 130 (👆), which is > 127 and should be highlighted red and shown to have produced the error.
          # Of course, this is all negated by using the flag 'no_chr_limit' as you can see in the if statement below.

          if value < 0 or (not self.flags.no_chr_limit and value > 127):
            distance = 0

            # Get distance between current `.` and the `.` before it.
            for j in range(i-1, -1, -1):
              if _code[j] == '.': break
              else:  distance += 1

            print(f"╭─ {value} out of range.\n╰─> {_code[:i-distance]}{Fore.RED}{_code[i-distance:i]}.{Fore.RESET}{_code[i+1:]}")
            if not self.flags.no_exit: exit(1)

          else:
            char = chr(self.data[self.pointer])

            self.op.write(char)
            if not self.flags.no_stdout: print(char)

        case ',':
          uinput: int | None = None

          while uinput is None:
            try: uinput = int(input("Input: "))
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

  def ttc(self, _text: str) -> str:
    """ Text To Code. """

    code = StringIO()
    iterc, incrs, extra = StringIO(), StringIO(), StringIO()

    for c in _text:
      v = ord(c)
      i = v // 10

      if v < 0 or (not self.flags.no_chr_limit and v > 127):
        print(f"{v} out of range ('{c}').")
        exit(1)

      itercount = i + (10 - (v % 10)) if v % 10 > 5 else i + (5 - (v % 5)) if v % 5 >= 5 else i
      vv = itercount * i

      if not v == vv:
        global diff; diff = abs((v - vv) if v > vv else (vv - v))
        extra.write(''.join(['+' if v > vv else '-' for _ in range(diff)]))

      print(itercount, v, vv, diff)

      iterc.write(''.join(['+' for _ in range(itercount)]))
      incrs.write(''.join(['+' for _ in range(i)]))
      code.write(f"{'>' if '.' not in code.getvalue() else ">>"}{iterc.getvalue()}[<{incrs.getvalue()}>-]<{extra.getvalue()}.")

      self._clear_strios(iterc, incrs, extra)
    return code.getvalue()

  def dump(self, _path: str) -> None:
      with open(_path, 'w' if exists(_path) else  'x') as dmpfile: dmpfile.write(str(self.data)[1:-1])  # [1:-1] removes [ and ].
      print("Successfully dumped data to '%s'." %_path)

  def find(self, target: str | int) -> None:
    if type(target) == int: ...
    else: ...

  def format(self, _path: str) -> None:
    ml = self.flags.max_len
    if ml is None: ml = 50

    if not exists(_path):
      print("Cannot format `` because it doesn't exist.")
      exit(1)

    chars = "><+-.,[]"
    code = StringIO()

    with open(_path, 'r') as bffile:
      for c in bffile.read():
        if ml > 0 and len(code.getvalue()) % ml == 0: code.write('\n')
        if c in chars: code.write(c)

    with open(_path, 'w') as bffile: bffile.write(code.getvalue().strip())

    print("Formatted %s successfully." %_path)
    exit(0)

  def output(self, _path: str) -> None:
    with open(_path, 'w' if exists(_path) else 'x') as opfile: opfile.write(self.op.getvalue())
    print("Successfully wrote output to '%s'." %_path)
