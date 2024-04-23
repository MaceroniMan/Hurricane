import random

from hurricane.const import WIDTH

def wait():
  input("...")

def word_wrap(text, checkchar="", wrapchar="\n"):
  cnt = 0
  newouttext = ""
  
  for currchar in text:
    
    if currchar == checkchar:
      newouttext += currchar
      cnt = 0
      
    elif cnt == WIDTH:
      if currchar == " ":
        newouttext += wrapchar
        cnt = 0
      else:
        newouttext += currchar
    else:
      cnt += 1
      newouttext += currchar

  return newouttext

def replace_in_strings(text, player, screen):
  text = text.replace("[@]", player["name"].title())
  text = text.replace("R{", screen.red)
  text = text.replace("B{", screen.blue)
  text = text.replace("G{", screen.green)
  text = text.replace("Y{", screen.yellow)
  text = text.replace("}", screen.normal)
  return text

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