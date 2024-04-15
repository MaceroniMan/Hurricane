import hurricane.data.colors as colors
import hurricane.utils as utils

class menu(object):
  def __init__(self, string, layout, dslayout=None):
    self.menuString = string
    self.menuLayout = layout

    if dslayout == None:
      self.displayLayout = layout
    else:
      self.displayLayout = dslayout
    
    self.cords = [0, 0]
    self.value = None
    self.niceValue = None

    self.colors = colors.getcolors()

  def isin(self, x, y):
    try:
      if x < 0:
        return False
      elif y < 0:
        return False
      elif self.menuLayout[x][y] == "":
        return False
      else:
        return True
    except IndexError:
      return False

  def find(self, name=None):
    for x in range(len(self.displayLayout)):
      column = self.displayLayout[x]
      for y in range(len(column)):
        value = column[y]
        try:
          if value != "":
            if value == name or name == None:
              self.cords = [x, y]
              return # return on first entry
        except IndexError:
          pass
  
  def up(self):
    self.cords[1] -= 1
    if not self.isin(self.cords[0], self.cords[1]):
      self.cords[1] += 1

  def down(self):
    self.cords[1] += 1
    if not self.isin(self.cords[0], self.cords[1]):
      self.cords[1] -= 1

  def left(self):
    self.cords[0] -= 1
    if not self.isin(self.cords[0], self.cords[1]):
      self.cords[0] += 1

  def right(self):
    self.cords[0] += 1
    if not self.isin(self.cords[0], self.cords[1]):
      self.cords[0] -= 1

  def enter(self):
    print("")
    try:
      self.value = self.menuLayout[self.cords[0]][self.cords[1]]
      self.niceValue = self.displayLayout[self.cords[0]][self.cords[1]]
    except IndexError:
      self.value = False
      self.niceValue = False

  def registerkey(self, key, keylayout=None):
    if keylayout == None:
      keylayout = {
        "w": "up",
        "s": "down",
        "a": "left",
        "d": "right",
        "KEY_UP": "up",
        "KEY_DOWN": "down",
        "KEY_LEFT": "left",
        "KEY_RIGHT": "right",
        "KEY_ENTER": "enter",
        "KEY_ESC": "enter",
        "": "enter",
        " ": "enter"
      }
    if key in keylayout:
      if keylayout[key] == "up":
        self.up()
      elif keylayout[key] == "down":
        self.down()
      elif keylayout[key] == "left":
        self.left()
      elif keylayout[key] == "right":
        self.right()
      elif keylayout[key] == "enter":
        self.enter()
  
  def get(self):
    returnmenu = self.menuString
    
    for x in range(len(self.displayLayout)):
      column = self.displayLayout[x]
      for y in range(len(column)):
        value = utils.replaceinstrings(column[y], {"name":""})
        replacevalue = self.menuLayout[x][y]
        if self.cords[0] == x and self.cords[1] == y:
          returnmenu = returnmenu.replace("{" + replacevalue + "}", self.colors["background"] + value + self.colors["reset"])
        else:
          returnmenu = returnmenu.replace("{" + replacevalue + "}", value)
    
    return returnmenu