import hurricane.menu as menu
import hurricane.cmds as cmds
import hurricane.utils as utils
import hurricane.const as const
import hurricane.scripts as scripts
import hurricane.savegame as savegame
import hurricane.data.colors as colors

import copy
import math

def say(player, saylist):
  for i in saylist:
    if utils.parsecondition(i[0], player):
      utils.typing(i[1], player)
      utils.wait()
      return

def unlockchest(player, room, containers, items):
  utils.clear()
  if utils.parsecondition(room["container"]["condition"], player):
    if not player["location"] in player["containers"]:
      say(player, room["container"]["say"])
      player["containers"][player["location"]] = copy.deepcopy(containers[player["location"]])
    else: # below may want to be taken out
      utils.typing("The chest is already unlocked", player)
      utils.wait()
      
    scripts.inventory(player, room, containers, items)

def itemproperties(item, items, player):
  itemprop = items[item]
  if itemprop["value"] <= 1:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth almost nothing", player)
  else:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth maybe " + str(itemprop["value"]) + " stars.", player)
  utils.wait()

def dostables(player, world):
  c = colors.getcolors()

  if len(player["stables"]) == 0: # there are no stables to travel to
    print("There are no stables to travel to yet")
    utils.wait()
    return
  
  roomname = world[player["location"]]["name"]
  menustring = " Use " + roomname + " Stables \n"
  menustring += "==============" + "="*len(roomname) + "\n"

  reglist = []
  dislist = []
  
  for stablelocation in player["stables"]:
    if stablelocation != player["location"]:
      menustring += "Travel to '{" + stablelocation + "}'\n"
      reglist.append(stablelocation)
      dislist.append(world[stablelocation]["name"])
    else:
      menustring += "Travel to '" + world[stablelocation]["name"] + "' " + c["green"] + "(HERE)\n" + c["reset"]
  
  stableMenu = menu.menu(menustring, [reglist], [dislist])
  keypress = None

  stableMenu.find()
  
  while stableMenu.value == None:
    utils.clear()
    print(stableMenu.get())

    keypress = utils.getch(": ")
    
    stableMenu.registerkey(keypress, {"w":"up", "s":"down", "a":"left", "d":"right", "":"enter", "`":"enter"})
  
  place = stableMenu.value
  if keypress == "`":
    return None # if exited the menu
  elif place == False:
    return None # if nothing was selected
  else:
    utils.clear()
    player["location"] = place
    utils.typing("Travling to " + world[place]["name"], player, speed=.3)

def seequests(player, quests):
  donequests = ""
  notquests = ""
  
  if len(player["quests"]) > 0:
    for qid in player["quests"]:
      if player["quests"][qid] == len(quests[qid]["points"]): # check if the quest is compleated (1 past length of quest list)
        donequests += utils.wrapprint(quests[qid]["name"] + ": " + utils.replaceinstrings(quests[qid]["done"], player) + "\n\n", const.WIDTH)
      else:
        notquests += utils.wrapprint(quests[qid]["name"] + ": " + utils.replaceinstrings(quests[qid]["points"][player["quests"][qid]], player) + "\n\n", const.WIDTH)
  else:
    notquests += "No quests yet, go explore!"

  utils.clear()
  print(" Current Quests")
  print("================")
  print(notquests, end="", flush=True)

  if donequests != "":
    print("")
    print(" Compleated Quests")
    print("===================")
    print(donequests, end="", flush=True)
  
  utils.wait()

def game(player, items, npcs, world, quests, containers, userdata):
  while True:
    utils.clear()
    cr = world[player["location"]]

    # last part of logic will not run the random function if the room
    # has NOT changed
    currentnpcs = utils.npcs(player, npcs)
  
    player["moves"] += 1

    savegame.save(userdata[0], userdata[1], player)

    if "introtext" in cr:
      say(player, cr["introtext"])

    if "do" in cr:
      for i in cr["do"]:
        if utils.parsecondition(i[0], player):
          utils.parsedo(i[1], player)
          break
  
    if not player["location"] in player["world"]:
      player["world"][player["location"]] = []
    
    utils.clear()
    
    print(" " + cr["name"])
    print("="*(len(cr["name"])+2) + "\n")

    outtext = ""

    outtext += cr["desc.long"] + ". "

    if "store" in cr:
      if utils.parsecondition(cr["store"]["condition"], player):
        outtext += cr["store"]["desc"] + ". "

    if "stable" in cr:
      if not player["location"] in player["stables"]:
        player["stables"].append(player["location"])
      outtext += cr["stable"] + ". "

    if "container" in cr:
      outtext += cr["container"]["desc"] + ". "

    for a_npc in currentnpcs:
      for obps in currentnpcs[a_npc][0]["observation"]:
        if utils.parsecondition(obps[0], player):
          outtext += obps[1] + ". "
          break

    grounditems = player["world"][player["location"]]
    preface = ""
    postface = ""

    for gitem in range(len(grounditems)):
      if gitem == 0:
        preface = "A "
      elif gitem == len(grounditems)-1: # if its the last item
        preface = ", and a "
      else:
        preface = ", "

      if gitem == len(grounditems)-1: # if its the last item
        postface = " sits on the ground."
      else:
        postface = ""
        
      outtext += preface + items[grounditems[gitem]]["name"] + postface

    newouttext = utils.wrapprint(utils.replaceinstrings(outtext, player), const.WIDTH)
        
    print(newouttext + "\n")
  
    print("You can go:")
  
    for direction in cr["dirs"]:
      dirctn = cr["dirs"][direction]
      print("  " + direction.capitalize() + ": " + world[dirctn["dest"]]["name"] + " - " + world[dirctn["dest"]]["desc.short"]) # add in the locked door
  
    print("")
    
    userinput = input(": ")

    command = cmds.parse(userinput, player, currentnpcs)

    if command[0] == "EXT":
      utils.clear()
      print("Are you sure you want to exit?")
      if utils.prompt():
        return # exit gameloop
    elif command[0] == "NAC":
      utils.typing("unknown command", player)
      utils.wait()
    elif command[0] == "go":
      print()
      if command[1] in cr["dirs"]:
        dr = cr["dirs"][command[1]]
        if utils.parsecondition(dr["condition"], player):
          say(player, dr["say"])
          utils.parsedo(dr["do"], player)
          player["location"] = dr["dest"]
        else:
          say(player, dr["say"])
      else:
        utils.typing("You cannot go that way", player)
        utils.wait()
    elif command[0] == "inventory":
      scripts.inventory(player, cr, containers, items)
    elif command[0] == "unlock":
      if "container" in cr:
        unlockchest(player, cr, containers, items)
      else:
        utils.typing("There is nothing to open here", player)
        utils.wait()
    elif command[0] == "talk":
      if command[1] == None:
        if len(currentnpcs) != 0:
          # maybe implement a better way to do multi npc
          utils.typing("To many options to talk to, be more specific", player)
          utils.wait()
        else:
          utils.typing("Who are you talking to?", player)
          utils.wait()
      else:
        scripts.dialouge(currentnpcs[command[1]], player, quests)
    elif command[0] == "quests":
      seequests(player, quests)
    elif command[0] == "stable":
      dostables(player, world)
    elif command[0] == "store":
      if "store" in cr:
        if utils.parsecondition(cr["store"]["condition"], player):
          storedict = {
            "pricemultiplier" : cr["store"]["multiplier"],
            "items" : []
          }
          for i in cr["store"]["items"]:
            if utils.parsecondition(i[0], player):
              storedict["items"].append(i[1])
          scripts.storemenu(player, items, storedict)
        else:
          utils.typing("The store seems to be closed", player)
          utils.wait()
      else:
        utils.typing("There is not store here", player)
        utils.wait()