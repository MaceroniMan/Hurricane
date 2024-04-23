import blessed, sys

import hurricane.menu as menu
import hurricane.utils as utils

class Terminal(blessed.Terminal):
  def __init__(self):
    super().__init__()

  def prompt(self, text=""):
    invMenu = menu.menu(text + "{yes}   {no}", [["yes"], ["no"]], [["Yes"], ["No"]])

    invMenu.find()

    with self.hidden_cursor():
      while invMenu.value == None:
        print("\r" + invMenu.get(), end="")

        invMenu.registerkey(self.getchar())

    if invMenu.value == "yes":
      return True
    else:
      return False

  def getchar(self):
    with self.cbreak():
      code = self.inkey()
      if code.is_sequence:
        keypress = code.name
      else:
        keypress = code
    return keypress

  def typing(self, words, player=None, speed=.03, skip=True):
    if player != None:
      words = utils.replace_in_strings(words, player, self)
    newlines = 1

    for char in words:
      val = self.inkey(timeout=speed)
      if skip and val:
        print("\033[F"*newlines + words.replace("`", "\n"))
        return True
      if char == "`":
        input("")
        newlines += 1
      else:
        sys.stdout.write(char)
        sys.stdout.flush()
    print("")
    return False
  
  def cinput(self, prompt, hide=False):
    input_string = []
    pos = 0
  
    print("\r" + prompt + "".join(input_string) + self.on_white(" "), end="")
  
    with self.hidden_cursor():
      while True:
        with self.cbreak():
          code = self.inkey()
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
            print("\r" + prompt + "".join(input_string) + self.on_white(" ") + " ", end="")
          else:
            previous_char = input_string[pos]
            input_string[pos] = self.on_white(input_string[pos])
  
            print("\r" + prompt + "".join(input_string) + " ", end="")
  
            input_string[pos] = previous_char