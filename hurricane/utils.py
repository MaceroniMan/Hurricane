import os, time, select, sys, random, blessed
import hurricane.data.colors
import hurricane.menu as menu

def wait():
  input("...")

def prompt(term, text=""):
  invMenu = menu.menu(text + "{yes}   {no}", [["yes"], ["no"]], [["Yes"], ["No"]])

  invMenu.find()
  
  while invMenu.value == None:
    print("\r" + invMenu.get(), end="")

    invMenu.registerkey(getch(term))

  if invMenu.value == "yes":
    return True
  else:
    return False

def clear():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

def wrapprint(text, charlength, checkchar="", wrapchar="\n"):
  cnt = 0
  newouttext = ""
  
  for currchar in text:
    
    if currchar == checkchar:
      newouttext += currchar
      cnt = 0
      
    elif cnt == charlength:
      if currchar == " ":
        newouttext += wrapchar
        cnt = 0
      else:
        newouttext += currchar
    else:
      cnt += 1
      newouttext += currchar

  return newouttext

def replaceinstrings(text, player):
  c = hurricane.data.colors.getcolors()
  text = text.replace("[@]", player["name"].title())
  text = text.replace("R{", c["red"])
  text = text.replace("B{", c["blue"])
  text = text.replace("G{", c["green"])
  text = text.replace("Y{", c["green"])
  text = text.replace("}", c["reset"])
  return text

def getch(term):
  with term.cbreak():
    code = term.inkey()
    if code.is_sequence:
      keypress = code.name
    else:
      keypress = code
  return keypress

def typing(words, term, player=None, speed=.03, skip=True):
  if player != None:
    words = replaceinstrings(words, player)
  newlines = 1
  
  for char in words:
    val = term.inkey(timeout=speed)
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

def old_typing(words, player=None, speed=0.03, skip=True):
  if player != None:
    words = replaceinstrings(words, player)
  inputs = 1
  for char in words:
    if skip:
      i, o, e = select.select([sys.stdin], [], [], speed)
      if (i):
        if sys.stdin.readline().strip() == '':
          print('\033[F'*inputs + words.replace('`', '\n'))
          return True
    else:
      time.sleep(speed)
    if char == '`':
      input('')
      inputs += 1
    else:
      sys.stdout.write(char)
      sys.stdout.flush()
  print("")
  return False

# returns a list of the npcs in the current room
"""
{
  "npc_name" : [npcdict, dialouge_start]
}
"""

def npcs(game):
  returnnpcs = {}
  for npc in game.npcs:
    done = False
    for room in game.npcs[npc]:
      roomvalue = None
      if room == game.player["location"]:
        if isinstance(game.npcs[npc][room], str):
          roomvalue = game.npcs[npc][room]
        else:
          roomvalue = room
      
      if roomvalue != None:
        for condition in game.npcs[npc][roomvalue]["conditions"]:
          if parsecondition(condition[0], game.player):
            returnnpcs[npc] = [game.npcs[npc][roomvalue], condition[1]]
            done = True
            break

      if done:
        break
          
  return returnnpcs
  
# returns the player and whether or not exit was in the value
def parsedo(string, player):
  returnstring = "NA"
  if string == "":
    return returnstring
  items = string.split("|")
  for item in items:
    currentitem = [i for i in item.split(" ") if i != ''] # remove any blank items
    if currentitem[0] == "give":
      player["inventory"].append(currentitem[1])
    elif currentitem[0] == "set":
      player["flags"][currentitem[1]] = currentitem[2]
    elif currentitem[0] == "stars":
      player["stars"] += int(currentitem[1])
    elif currentitem[0] == "quest":
      player["quests"][currentitem[1]] = int(currentitem[2])
      returnstring = currentitem[1]
    elif currentitem[0] == "exit": # a hard end
      return "EXT"
  return returnstring

# returns true or false
def parsecondition(string, player):
  # this function will not fit into a lambda
  def flag(x, y="1"):
    if x in player["flags"]:
      return str(player["flags"][x]) == str(y)
    else:
      return False

  def quest(x):
    if x in player["quests"]:
      return int(player["quests"][x])
    else:
      return -1

  evalscope = {
    "has" : lambda x: x in player["inventory"],
    "flag" : flag,
    "random" : lambda x: random.randint(1,x) == 1,
    "quest" : quest,
    
    "stars" : player["stars"],
    "true" : True,
    "false" : False
  }
  
  return eval(string, evalscope)