from flags import Flags
from io import StringIO
from os.path import exists


class Interpreter:
  def __init__(self, _flags: Flags) -> None:
    self.data = [0]
    self.pointer = 0
    self.op = StringIO()
    self.flags = _flags

  def parse_code(self, _code: str) -> tuple[list[int], int]:
    i, loopstart = 0, 0

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

  def dump(self, _path: str) -> None:
      with open(_path, 'w' if exists(_path) else  'x') as dmpfile: dmpfile.write(str(self.data)[1:-1])  # [1:-1] removes [ and ].
      print("Successfully dumped data to '%s'." %_path)

  def output(self, _path: str) -> None:
    with open(_path, 'w' if exists(_path) else 'x') as opfile: opfile.write(self.op.getvalue())
    print("Successfully wrote output to '%s'." %_path)
