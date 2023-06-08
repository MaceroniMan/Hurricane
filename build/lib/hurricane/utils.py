import os, time, select, sys, random
import hurricane.data.getch
import hurricane.data.colors
import hurricane.menu as menu

def prompt():
  invMenu = menu.menu("{yes}   {no}", [["yes"], ["no"]], [["Yes"], ["No"]])

  invMenu.find()
  
  while invMenu.value == None:
    print("\r" + invMenu.get(), end="")

    keypress = getch("")

    invMenu.registerkey(keypress)

  if invMenu.value == "yes":
    return True
  else:
    return False

def getch(p=">> "):
  return hurricane.data.getch.getch(p)

def clear():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

def replaceinstrings(text, player):
  c = hurricane.data.colors.getcolors()
  text = text.replace("[@]", player["name"].title())
  text = text.replace("R{", c["red"])
  text = text.replace("B{", c["blue"])
  text = text.replace("G{", c["green"])
  text = text.replace("Y{", c["green"])
  text = text.replace("}", c["reset"])
  return text

def typing(words, player, speed=0.03, skip=True):
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

def npcs(player, npcs):
  returnnpcs = {}
  for npc in npcs:
    done = False
    for room in npcs[npc]:
      roomvalue = None
      if room == player["location"]:
        if isinstance(npcs[npc][room], str):
          roomvalue = npcs[npc][room]
        else:
          roomvalue = room
      
      if roomvalue != None:
        for condition in npcs[npc][roomvalue]["conditions"]:
          if parsecondition(condition[0], player):
            returnnpcs[npc] = [npcs[npc][roomvalue], condition[1]]
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