from flags import Flags
from io import StringIO
from math import sqrt
from os.path import exists


class Interpreter:
  def __init__(self, _flags: Flags) -> None:
    self.data = [0]
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

    for i, c in enumerate(_text):
      v = ord(c)
      vroot = int(sqrt(v))

      if v < 0 or (not self.flags.no_chr_limit and v > 127):
        print(f"{v} out of range ('{c}').")
        exit(1)

      itercount = vroot
      incrcount = int(v / vroot)
      vv = itercount * incrcount

      if not v == vv:
        if v < vv: extra.write(''.join(['-' for _ in range(vv - v)]))
        elif v > vv: extra.write(''.join(['+' for _ in range(v - vv)]))

      iterc.write(''.join(['+' for _ in range(itercount)]))
      incrs.write(''.join(['+' for _ in range(incrcount)]))
      code.write(f"{'>' if '.' not in code.getvalue() else ">>"}{iterc.getvalue()}[<{incrs.getvalue()}>-]<{extra.getvalue()}.")

      self._clear_strios(iterc, incrs, extra)
    return code.getvalue()

  def dump(self, _path: str) -> None:
      with open(_path, 'w' if exists(_path) else  'x') as dmpfile: dmpfile.write(str(self.data)[1:-1])  # [1:-1] removes [ and ].
      print("Successfully dumped data to '%s'." %_path)

  def output(self, _path: str) -> None:
    with open(_path, 'w' if exists(_path) else 'x') as opfile: opfile.write(self.op.getvalue())
    print("Successfully wrote output to '%s'." %_path)
