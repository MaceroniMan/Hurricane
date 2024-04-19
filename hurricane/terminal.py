import blessed

class Terminal(blessed.Terminal):
  def __init__(self):
    super().__init__()

def cinput(term, prompt, hide=False):
  input_string = []
  pos = 0

  print("\r" + prompt + "".join(input_string) + term.on_white(" "), end="")

  with term.hidden_cursor():
    while True:
      with term.cbreak():
        code = term.inkey()
        if code.is_sequence:
          keypress = code.name
          if keypress == "KEY_LEFT":
            if pos > 0:
              pos -= 1
          elif keypress == "KEY_RIGHT":
            if pos < len(input_string):
              pos += 1
          elif keypress == "KEY_BACKSPACE":
            if pos > 0:
              input_string = input_string[:pos-1] + input_string[pos:]
              pos -= 1
          elif keypress == "KEY_ENTER":
            print("\r" + prompt + "".join(input_string) + "  ")
            return "".join(input_string)
          elif keypress == "KEY_ESCAPE":
            print("\r" + prompt + "".join(input_string) + "  ")
            return None
        else:
          input_string.insert(pos, code)
          pos += 1

      if not hide:
        if pos == len(input_string): # if the position is at end of string
          print("\r" + prompt + "".join(input_string) + term.on_white(" ") + " ", end="")
        else:
          previous_char = input_string[pos]
          input_string[pos] = term.on_white(input_string[pos])

          print("\r" + prompt + "".join(input_string) + " ", end="")

          input_string[pos] = previous_char