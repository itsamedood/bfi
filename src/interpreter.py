from colorama import Fore
from flags import CharAction, Flags
from io import StringIO
from math import sqrt
from os.path import exists
from re import match
from sys import exit


class Interpreter:
  """ Interprets Brainfuck code and can do a few other things. """

  def __init__(self, _flags: Flags) -> None:
    self.data = [0] if _flags.max_size is None else [0 for _ in range(_flags.max_size)]
    self.pointer = 0
    self.op = StringIO()
    self.flags = _flags

    self.forward, self.backward, self.increment, self.decrement, self.print, self.input, self.loop_start, self.loop_end = [char for char in _flags.bfcharset.values()]
    # print([v for v in _flags.bfcharset.values()])

  def _clear_strios(self, *strios: StringIO) -> None:
    for strio in strios:
      strio.seek(0)
      strio.truncate(0)

  def parse_code(self, _code: str) -> tuple[list[int], int]:
    """ Parses given code, ignoring any invalid characters. """

    i, loopstart = 0, 0
    errord = False

    # Use a while loop since it allows us to jump back x characters for looping.
    while i < len(_code):
      c = _code[i]

      match c:
        case self.forward:
          self.pointer += 1

          if len(self.data) < self.pointer + 1:
            if self.flags.max_size is not None and len(self.data) == self.flags.max_size:
              if not errord:
                print(f"╭─ Cannot exceed max size of {self.flags.max_size}.\n╰─> {''.join([f"{Fore.RED}{l}{Fore.RESET}" if j == i else l for j, l in enumerate(_code)])}")
                errord = True

              if not self.flags.no_exit: exit(1)
              self.pointer -= 1

            else: self.data.append(0)

        case self.backward:
          if self.pointer > 0: self.pointer -= 1

        case self.increment: self.data[self.pointer] += 1

        case self.decrement: self.data[self.pointer] -= 1

        case self.print:
          value = self.data[self.pointer]

          # >++++++++[<+++++++++>-]<.>>+++++++++++++[<++++++++++>-]<.>>++++++++[<+++++++++>-]<.
          #                          👆                             👆
          # The statement pointed at above produces 130, which is > 127,
          # and should be highlighted red and shown to have produced the error.
          # Can be negated by using the flag 'no_chr_limit' as seen in the if statement below.

          # Highlight code that produced bad value and highlight it red.
          if value < 0 or (not self.flags.no_chr_limit and value > 127):
            distance = 0

            # Get distance between current `.` and the `.` before it.
            for j in range(i-1, -1, -1):
              if _code[j] == '.': break
              else:  distance += 1

            print(f"\n╭─ {value} out of range.\n╰─> {_code[:i-distance]}{Fore.RED}{_code[i-distance:i]}.{Fore.RESET}{_code[i+1:]}")
            if not self.flags.no_exit: exit(1)

          else:
            char = chr(self.data[self.pointer])

            self.op.write(char)
            if not self.flags.no_stdout: print(char, end='')

        case self.input:  # Honestly who even uses this.
          uinput: str | int | None = None

          while uinput is None:
            uinput = input("Input: ")

            # Condensing like a dozen lines of code to 3 is the BEST feeling.
            if match(r"^[0-9]*", uinput): uinput = int(uinput)
            elif self.flags.no_strict_input and match(r"^[^\d]$", uinput): uinput = ord(uinput)
            else: uinput = None

          self.data[self.pointer] = uinput

        case self.loop_start:
          if self.loop_end not in _code:
            print("Loop never closed.")
            break

          else: loopstart = i

        case self.loop_end:
          if not self.data[self.pointer] == 0: i = loopstart

      i += 1

    print('\n', end='')
    return (self.data, self.pointer)

  def ttc(self, _text: str) -> str:
    """ Text To Code, converts regular text to Brainfuck code. """

    code = StringIO()
    # iterc, incrs, extra = StringIO(), StringIO(), StringIO()

    for c in _text:
      v = ord(c)

      if v < 0 or (not self.flags.no_chr_limit and v > 127):
        print(f"{v} out of range ('{c}').")
        exit(1)

      prime = True
      best: tuple[int, int, int]
      min_diff = float("inf")

      # First we check if it's a prime number like 101, since we don't want (1, 101).
      if v > 2:
        for i in range(2, int(sqrt(v)) + 1):
          if v % i == 0:
            prime = False
            break

        if prime:
          v -= 1
          k = 1
        else: k = 0


      # Now we do fancy(ish) math to determine best nums for multiplying and having a clean amount of `+`s.
      # It works well most of the time 🤷‍♂️.
      for i in range(1, v+1):
        if v % i == 0:
          j = v // i
          diff = abs(i - j)

          if diff < min_diff:
            min_diff = diff
            best = (i, j, k)

      # print(f"BEST NUMS FOR {v}: ({best[0]}, {best[1]})")

      iterc, incrs, extra = best
      code.write(f"{'>' if '.' not in code.getvalue() else ">>"}{''.join(['+' for _ in range(iterc)])}[<{''.join(['+' for _ in range(incrs)])}>-]<{''.join(['+' if extra > 0 else '-' for _ in range(extra)])}.")

    return code.getvalue()

  def dump(self, _path: str) -> None:
      """ Dump the data (memory, if you will) into the specified file. """

      with open(_path, 'w' if exists(_path) else  'x', encoding="utf-8") as dmpfile: dmpfile.write(str(self.data)[1:-1])  # [1:-1] removes [ and ].
      print("Successfully dumped data to '%s'." %_path)

  def find(self, target: str | int) -> None:
    """ Find a specific character by it's value or number and highlight it. """

    if type(target) == int: ...
    else: ...

  def format(self, _path: str) -> None:
    """ Formats a `.bf` file, which involves removing all characters that are not part of Brainfuck. """

    ml = self.flags.max_len
    if ml is None: ml = 50

    if not exists(_path):
      print("Cannot format '%s' because it doesn't exist." %_path)
      exit(1)

    chars = "><+-.,[]"
    code = StringIO()

    with open(_path, 'r') as bffile:
      for c in bffile.read():
        if ml > 0 and len(code.getvalue()) % ml == 0: code.write('\n')
        if c in chars: code.write(c)

    with open(_path, 'w', encoding="utf-8") as bffile: bffile.write(code.getvalue().strip())

    print("Formatted %s successfully." %_path)
    exit(0)

  def output(self, _path: str) -> None:
    """ Dump the output into a file. The output is comprised of every time you print a value using `.`. """

    with open(_path, 'w' if exists(_path) else 'x', encoding="utf-8") as opfile: opfile.write(self.op.getvalue())
    print("Successfully wrote output to '%s'." %_path)
