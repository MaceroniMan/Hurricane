import hurricane.data.colors as colors
import hurricane.utils as utils

class layouts():
  STD = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
    "KEY_UP": "up",
    "KEY_DOWN": "down",
    "KEY_LEFT": "left",
    "KEY_RIGHT": "right",
    "KEY_ENTER": "enter",
    "KEY_ESCAPE": "enter",
    "": "enter",
    " ": "enter"
  }

  NOESC = {
    "w": "up",
    "s": "down",
    "a": "left",
    "d": "right",
    "KEY_UP": "up",
    "KEY_DOWN": "down",
    "KEY_LEFT": "left",
    "KEY_RIGHT": "right",
    "KEY_ENTER": "enter"
  }

class menu(object):
  def __init__(self, string, layout, dslayout=None):
    self.menu_string = string
    self.menu_layout = layout

    if dslayout == None:
      self.display_layout = layout
    else:
      self.display_layout = dslayout
    
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
      elif self.menu_layout[x][y] == "":
        return False
      else:
        return True
    except IndexError:
      return False

  def find(self, name=None):
    for x in range(len(self.display_layout)):
      column = self.display_layout[x]
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
      self.value = self.menu_layout[self.cords[0]][self.cords[1]]
      self.niceValue = self.display_layout[self.cords[0]][self.cords[1]]
    except IndexError:
      self.value = False
      self.niceValue = False

  def registerkey(self, key, key_layout=None):
    if key_layout == None:
      key_layout = layouts.STD
      
    if key in key_layout:
      if key_layout[key] == "up":
        self.up()
      elif key_layout[key] == "down":
        self.down()
      elif key_layout[key] == "left":
        self.left()
      elif key_layout[key] == "right":
        self.right()
      elif key_layout[key] == "enter":
        self.enter()
        self.prev_key = key
  
  def get(self):
    returnmenu = self.menu_string
    
    for x in range(len(self.display_layout)):
      column = self.display_layout[x]
      for y in range(len(column)):
        value = utils.replaceinstrings(column[y], {"name":""})
        replacevalue = self.menu_layout[x][y]
        if self.cords[0] == x and self.cords[1] == y:
          returnmenu = returnmenu.replace("{" + replacevalue + "}", self.colors["background"] + value + self.colors["reset"])
        else:
          returnmenu = returnmenu.replace("{" + replacevalue + "}", value)
    
    return returnmenu