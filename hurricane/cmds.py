def splitlist(old):
  new = []
  reflist = []
  for i in old:
    addlist = [x.lower() for x in i.split(" ")]
    for p in range(len(addlist)):
      reflist.append(i)
    new += addlist
  return new, reflist

def parse(command, player, npcs):
  command = command.lower()
  command = command.replace("?", "")
  actionlist = list(command.split(" "))

  verb = None
  validsubjects = []
  reflist = []
  
  for word in actionlist:
    if verb != None:
      if word in validsubjects:
        return [verb, reflist[validsubjects.index(word)]]
        
    elif word in ["talk"]:
      verb = "talk"
      validsubjects = [x for x in npcs]
      if len(validsubjects) == 1:
        return ["talk", validsubjects[0]]
      else:
        validsubjects, reflist = splitlist(validsubjects)
      
    elif word in ["north", "east", "south", "west"]:
      return ["go", word]
      
    elif word in ["go", "move", "walk", "run"]:
      verb = "go"
      validsubjects = ["north", "east", "south", "west"]
      reflist = ["north", "east", "south", "west"]
      
    elif word in ['inventory', 'bag', 'backpack']:
      return ["inventory"]
      
    elif word in ["unlock", "open", "look", "inspect"]:
      return ["unlock"]

    elif word in ["store"]:
      return ["store"]
      
    elif word in ["save", "savegame"]:
      return ["save"]

    elif word in ["quest", "quests", "status"]:
      return ["quests"]

    elif word in ["travel", "stable", "stables"]:
      return ["stable"]

    elif word in ['exit', 'quit', 'leave']:
      return ["EXT"]

  if verb == None:
    return ["NAC"]
  else:
    return [verb, None]