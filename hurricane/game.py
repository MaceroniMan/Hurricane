import menu
import cmds
import utils
import savegame

import data.htf as htf
import data.tutorial as tutorial

import os
import sys
import json
import copy

import math

KEY = "hurricane"

def wait():
  input("...")

def say(player, saylist):
  for i in saylist:
    if utils.parsecondition(i[0], player):
      utils.typing(i[1], player)
      wait()
      return

def unlockchest(player, room, containers, items):
  utils.clear()
  if utils.parsecondition(room["container"]["condition"], player):
    if not player["location"] in player["containers"]:
      say(player, room["container"]["say"])
      player["containers"][player["location"]] = copy.deepcopy(containers[player["location"]])
    else: # below may want to be taken out
      utils.typing("The chest is already unlocked", player)
      wait()
      
    inventory(player, room, containers, items)

def itemproperties(item, items, player):
  itemprop = items[item]
  if itemprop["value"] <= 1:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth almost nothing", player)
  else:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth maybe " + str(itemprop["value"]) + " stars.", player)
  wait()

"""
Store Dict:
{
  "pricemultiplier" : 0
  "name" : []
}
"""

def storemenu(player, items, storedict):
  utils.clear()

  done = False

  buyback = []

  while not done:
    maxinvlength = 9
    for i in player["inventory"]:
      nme = items[i]["name"]
      if len(nme) > maxinvlength:
        maxinvlength = len(nme)
    
    maxstolength = 5
    for i in storedict["items"]:
      nme = items[i]["name"]
      if len(nme) > maxstolength:
        maxstolength = len(nme)

    maxbuylength = 7
    for i in buyback:
      nme = items[i]["name"]
      if len(nme) > maxbuylength:
        maxbuylength = len(nme)

    inventorytitleminus = maxinvlength - 9
    storetitleminus = maxstolength - 5
    buybacktitleminus = maxbuylength - 7
    
    if maxinvlength % 2 == 0:
      maxinvlength += 1

    if maxstolength % 2 == 0:
      maxstolength += 1

    if maxbuylength % 2 == 0:
      maxbuylength += 1

    printstring = "Stars: " + str(player["stars"]) + "\n\n"

    reglist_inv = []
    reglist_sto = []
    reglist_buy = []

    dislist_inv = []
    dislist_sto = []
    dislist_buy = []
    
    printstring += "+-" + "-"*math.ceil(inventorytitleminus/2) + "inventory" + "-"*math.ceil(inventorytitleminus/2) + "-+-" + "-"*math.ceil(storetitleminus/2) + "store" + "-"*math.ceil(storetitleminus/2) + "-+-" + "-"*math.ceil(buybacktitleminus/2) + "buyback" + "-"*math.ceil(buybacktitleminus/2) + "-+" + "\n"

    maxlength = max([len(storedict["items"]), len(player["inventory"]), len(buyback)])+1

    printstring += "| " + " "*(maxinvlength) + " | " + " "*(maxstolength) + " | " + " "*(maxbuylength) + " |\n"

    for i in range(maxlength):
      if i < len(player["inventory"]):
        extraspaces = maxinvlength-len(items[player["inventory"][i]]["name"])
        printstring += "| " + " "*(extraspaces) + "{inv$" + player["inventory"][i] + "$" + str(i) + "} |"
        dislist_inv.append(items[player["inventory"][i]]["name"])
        reglist_inv.append("inv$" + player["inventory"][i] + "$" + str(i))
      else:
        printstring += "| " + " "*(maxinvlength) + " |"


      if i < len(storedict["items"]):
        extraspaces = maxstolength-len(items[storedict["items"][i]]["name"])
        printstring += " " + " "*(extraspaces) + "{sto$" + storedict["items"][i] + "$" + str(i) + "} |"
        dislist_sto.append(items[storedict["items"][i]]["name"])
        reglist_sto.append("sto$" + storedict["items"][i] + "$" + str(i))
      else:
        printstring += " " + " "*(maxstolength) + " |"

      if i < len(buyback):
        extraspaces = maxbuylength-len(items[buyback[i]]["name"])
        printstring += " " + " "*(extraspaces) + "{buy$" + buyback[i] + "$" + str(i) + "} |"
        dislist_buy.append(items[buyback[i]]["name"])
        reglist_buy.append("buy$" + buyback[i] + "$" + str(i))
      else:
        printstring += " " + " "*(maxbuylength) + " |"
  
      printstring += "\n" # end the line

    printstring += "+-" + "-"*(maxinvlength) + "-+-" + "-"*(maxstolength) + "-+-" + "-"*(maxbuylength) + "-+\n"
    
    invMenu = menu.menu(printstring, [reglist_inv, reglist_sto, reglist_buy], [dislist_inv, dislist_sto, dislist_buy])
    keypress = None

    invMenu.find()
    
    while invMenu.value == None:
      utils.clear()
      print(invMenu.get())

      keypress = utils.getch(": ")
      
      invMenu.registerkey(keypress, {"w":"up", "s":"down", "a":"left", "d":"right", "":"enter", "`":"enter"})
    
    item = invMenu.value.split("$")
    if keypress == "`":
      done = True
    else:
      if item[0] == "sto":
        stars = items[item[1]]["value"] * storedict["pricemultiplier"]
        print("Do you want to purchase a " + item[1] + " for " + str(stars) + " stars?")
        if utils.prompt():
          if stars > player["stars"]:
            print("You do not have enough stars!")
          else:
            player["stars"] -= stars
            player["inventory"].append(item[1])
            print("You purchased a " + item[1] + " for " + str(stars) + " stars")
      elif item[0] == "inv":
        stars = items[item[1]]["value"]
        print("Do you want to sell a " + item[1] + " for " + str(stars) + " stars?")
        if utils.prompt():
          print("You sold a " + item[1] + " for " + str(stars) + " stars")
          player["stars"] += stars
          player["inventory"].remove(item[1])
          buyback.append(item[1])
      elif item[0] == "buy":
        stars = items[item[1]]["value"]
        print("Do you want to purchase a " + item[1] + " for " + str(stars) + " stars?")
        if utils.prompt():
          if stars > player["stars"]:
            print("You do not have enough stars!")
          else:
            player["stars"] -= stars
            player["inventory"].append(item[1])
            buyback.remove(item[1])
            print("You purchased a " + item[1] + " for " + str(stars) + " stars")

def dostables(player, world):
  if len(player["stables"])-1 == 0: # there are no stables to travel to
    print("there are no stables to travel to yet")
    wait()
    return
  
  roomname = world[player["location"]]["name"]
  menustring = " Use " + roomname + " Stables \n"
  menustring += "==============" + "="*len(roomname) + "\n"

  reglist = []
  dislist = []
  
  for stablelocation in player["stables"]:
    if stablelocation != player["location"]:
      menustring += "Travel to {" + stablelocation + "}\n"
      reglist.append(stablelocation)
      dislist.append(world[stablelocation]["name"])
  
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
  else:
    utils.clear()
    player["location"] = place
    utils.typing("Travling to " + world[place]["name"], player, speed=.3)
  
def inventory(player, room, containers, items):
  # note: bag is the same as containers and chests
  utils.clear()

  done = False
  
  while not done:
    maxinvlength = 9
    for i in player["inventory"]:
      nme = items[i]["name"]
      if len(nme) > maxinvlength:
        maxinvlength = len(nme)

    maxgndlength = 6
    grounditems = copy.deepcopy(player["world"][player["location"]])
    for i in grounditems:
      nme = items[i]["name"]
      if len(nme) > maxgndlength:
        maxgndlength = len(nme)
  
    maxbaglength = None
    currentcontainer = []

    if "container" in room:
      if utils.parsecondition(room["container"]["condition"], player):
        if player["location"] in player["containers"]:
          currentcontainer = copy.deepcopy(player["containers"][player["location"]])
          
          maxbaglength = 5
          
          for i in currentcontainer:
            nme = items[i]["name"]
            if len(nme) > maxbaglength:
              maxbaglength = len(nme)

          containertitleminus = maxbaglength - 5
          
          if containertitleminus % 2 != 0:
            maxbaglength += 1
    
    if maxinvlength % 2 == 0:
      maxinvlength += 1

    if maxgndlength % 2 != 0:
      maxgndlength += 1

    inventorytitleminus = maxinvlength - 9
    groundtitleminus = maxgndlength - 6
    
    utils.clear()
  
    printstring = "Stars: " + str(player["stars"]) + "\n\n"
    reglist_inv = []
    reglist_bag = []
    reglist_gnd = []

    dislist_inv = []
    dislist_bag = []
    dislist_gnd = []

    bagtitlestring = ""
    
    if maxbaglength != None:
      bagtitlestring = "-" + "-"*math.ceil(containertitleminus/2) + "chest" + "-"*math.ceil(containertitleminus/2) + "-+"

    printstring += "+-" + "-"*math.ceil(inventorytitleminus/2) + "inventory" + "-"*math.ceil(inventorytitleminus/2) + "-+" + bagtitlestring + "-" + "-"*math.ceil(groundtitleminus/2) + "ground" + "-"*math.ceil(groundtitleminus/2) + "-+" + "\n"
  
    maxlength = max([len(currentcontainer), len(player["inventory"]), len(grounditems)])+1
  
    printstring += "| " + " "*(maxinvlength) + " |"
    if maxbaglength != None:
      printstring += " " + " "*(maxbaglength) + " |"
    printstring += " " + " "*(maxgndlength) + " |"
    printstring += "\n" # end the line
    
    for i in range(maxlength):
      if i < len(player["inventory"]):
        extraspaces = maxinvlength-len(items[player["inventory"][i]]["name"])
        
        printstring += "| " + " "*(extraspaces) + "{inv$" + player["inventory"][i] + "$" + str(i) + "} |"
        dislist_inv.append(items[player["inventory"][i]]["name"])
        reglist_inv.append("inv$" + player["inventory"][i] + "$" + str(i))
      else:
        printstring += "| " + " "*(maxinvlength) + " |"

      if i < len(currentcontainer):
        extraspaces = maxbaglength-len(items[currentcontainer[i]]["name"])
        
        printstring += " " + " "*(extraspaces) + "{bag$" + currentcontainer[i] + "$" + str(i) + "} |"
        dislist_bag.append(items[currentcontainer[i]]["name"])
        reglist_bag.append("bag$" + currentcontainer[i] + "$" + str(i))
      elif maxbaglength != None:
        printstring += " " + " "*(maxbaglength) + " |"

      if i < len(grounditems):
        extraspaces = maxgndlength-len(items[grounditems[i]]["name"])

        printstring += " " + " "*(extraspaces) + "{gnd$" + grounditems[i] + "$" + str(i) + "} |"
        dislist_gnd.append(items[grounditems[i]]["name"])
        reglist_gnd.append("gnd$" + grounditems[i] + "$" + str(i))
      else:
        printstring += " " + " "*(maxgndlength) + " |"
  
      printstring += "\n" # end the line
  
    if maxbaglength != None:
      printstring += "+-" + "-"*(maxinvlength) + "-+-" + "-"*(maxbaglength) + "-+-" + "-"*(maxgndlength) + "-+\n"
    else:
      printstring += "+-" + "-"*(maxinvlength) + "-+-" + "-"*(maxgndlength) + "-+\n"

    if len(reglist_bag) != 0:
      reglist = [reglist_inv, reglist_bag, reglist_gnd]
      dislist = [dislist_inv, dislist_bag, dislist_gnd]
    else:
      reglist = [reglist_inv, reglist_gnd]
      dislist = [dislist_inv, dislist_gnd]

    
    invMenu = menu.menu(printstring, reglist, dislist)
    keypress = None

    invMenu.find()

    currentoutputmenu = ""
    
    while invMenu.value == None:
      utils.clear()
      currentoutputmenu = invMenu.get()
      print(currentoutputmenu)

      keypress = utils.getch(": ")
      
      invMenu.registerkey(keypress, {"w":"up", "s":"down", "a":"left", "d":"right", "":"enter", " ":"enter", "`":"enter"})
    
    item = invMenu.value.split("$")
    if keypress == " ":
      movedone = False
      while not movedone:
        movedone = True # will set as false when moving items is done

        currentoutputmenu = currentoutputmenu.replace("-inventory-", "-{inventory}-").replace("-chest-", "-{chest}-").replace("-ground-", "-{ground}-")

        currentoutputmenu += "Where to move " + items[item[1]]["name"] + "?"

        if maxbaglength != None:
          reglist = [["inventory"], ["chest"], ["ground"]]
        else:
          reglist = [["inventory"], ["ground"]]
        
        moveMenu = menu.menu(currentoutputmenu, reglist)

        # autodefault menu to the current place
        findelement = None
        if item[0] == "gnd":
          findelement = "ground"
        elif item[0] == "bag":
          findelement = "chest"
        elif item[0] == "inv":
          findelement = "inventory"
        
        moveMenu.find(findelement)
    
        while moveMenu.value == None:
          utils.clear()
          print(moveMenu.get())
      
          moveMenu.registerkey(utils.getch(": "), {"w":"up", "s":"down", "a":"left", "d":"right", "":"enter", " ":"enter",})
        
        
        if moveMenu.value == "inventory":
          if item[0] == "gnd":
            player["inventory"].append(item[1])
            player["world"][player["location"]].remove(item[1])
          elif item[0] == "bag":
            player["inventory"].append(item[1])
            player["containers"][player["location"]].remove(item[1])
        elif moveMenu.value == "chest":
          if maxbaglength != None:
            if item[0] == "inv":
              player["containers"][player["location"]].append(item[1])
              player["inventory"].remove(item[1])
            elif item[0] == "gnd":
              player["containers"][player["location"]].append(item[1])
              player["world"][player["location"]].remove(item[1])
        elif moveMenu.value == "ground":
          if item[0] == "inv":
            player["world"][player["location"]].append(item[1])
            player["inventory"].remove(item[1])
          elif item[0] == "bag":
            player["world"][player["location"]].append(item[1])
            player["containers"][player["location"]].remove(item[1])
    elif keypress == "`":
      done = True
    else:
      itemproperties(item[1], items, player)

def seequests(player, quests):
  donequests = ""
  notquests = ""
  
  if len(player["quests"]) > 0:
    for qid in player["quests"]:
      if player["quests"][qid] == len(quests[qid]["points"]): # check if the quest is compleated (1 past length of quest list)
        donequests += wrapprint(quests[qid]["name"] + ": " + utils.replaceinstrings(quests[qid]["done"], player) + "\n\n", 70)
      else:
        notquests += wrapprint(quests[qid]["name"] + ": " + utils.replaceinstrings(quests[qid]["points"][player["quests"][qid]], player) + "\n\n", 70)
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
  
  wait()

def dialouge(npc, player, quests):
  dialougedict = npc[0]["dialouges"]
  talklocation = npc[1]
  starttext = ""

  while True:
    utils.clear()
    
    if not talklocation in dialougedict:
      raise ValueError(talklocation + " does not exist")
      
    dialougecurrent = dialougedict[talklocation]
    beforetext = ""

    if starttext != "":
      beforetext += starttext + "\n\n"
    
    for person_index in range(len(dialougecurrent["dialouge"])):
      utils.clear()
      print(utils.replaceinstrings(beforetext, player), end="", flush=True)
      
      person = dialougecurrent["dialouge"][person_index]
      print(person[0] + ": ", end="", flush=True)
      doneskip = utils.typing(person[1], player)
      if doneskip:
        utils.clear()
        print(utils.replaceinstrings(beforetext, player), end="", flush=True)
        print(person[0] + ": " + utils.replaceinstrings(person[1], player).replace("`", "\n"), end="", flush=True)
      
      beforetext += person[0] + ": " + person[1].replace("`", "\n") + "\n\n"
      if person_index+1 != len(dialougecurrent["dialouge"]):
        input()
      
    doext = utils.parsedo(dialougecurrent["do"], player)

    if doext == "EXT":
      input()
      break # end the dialouge menu
    elif doext != "NA":
      input() # add a extra pause in flow
      utils.clear()
      if player["quests"][doext] == 0: # if the quest was just given
        utils.typing("Quest '" + quests[doext]["name"] + "' received", player, speed=.1)
      elif player["quests"][doext] == len(quests[doext]["points"]): # if the quest was just compleated (1 past length of quest list)
        utils.typing("Quest '" + quests[doext]["name"] + "' compleated", player, speed=.1)
      else:
        utils.typing("Quest '" + quests[doext]["name"] + "' advanced", player, speed=.1)
      wait()
    
    if len(dialougecurrent["options"]) == 0:
      input()
      break
    else:
      optionstring = ""
      nicelist = [[]]
      optionlist = [[]]
    
      for option in dialougecurrent["options"]:
        if utils.parsecondition(option[0], player):
          optionstring += "{" + option[1]["goto"] + "}\n"
          nicelist[0].append(option[1]["text"])
          optionlist[0].append(option[1]["goto"])

      beforetext = utils.replaceinstrings(beforetext, player).replace("`", "\n")
      dialoueMenu = menu.menu(beforetext + optionstring, optionlist, nicelist)
    
      while dialoueMenu.value == None:
        utils.clear()
        print(dialoueMenu.get())

        dialoueMenu.registerkey(utils.getch(""))

      talklocation = dialoueMenu.value

    if talklocation == "exit":
      break # leave the menu
  
def startmenu():
  assets = json.loads(htf.decode("data/assets.dat", KEY))
  items = assets["items"]
  npcs = assets["npcs"]
  world = assets["world"]
  quests = assets["quests"]
  containers = assets["containers"]

  if not os.path.exists("saves"):
    os.makedirs("saves")

  action = None
  savegameresult = ""
  while action == None:
    menustr = """ Hurricane - Apple
===================
use keys 'w' 'a' 's' and 'd' to navigate the menu

'{load}' ....... load a saved game
'{start}' ...... start a new game
'{tutorial}' ... start a short tutorial
'{exit}' ....... exit the game"""
    mainMenu = menu.menu(menustr, [["load", "start", "tutorial", "exit"]])
    
    while mainMenu.value == None:
      utils.clear()
      print(mainMenu.get())

      mainMenu.registerkey(utils.getch(": "))
    
    menuinput = mainMenu.value
    if menuinput == "load":
      utils.clear()
      print(" Load a Existing Saved Game")
      print("============================")
      username = input("saved game name: ")
      password = input("password: ")
      if username == "":
        action = None
        savegameresult = None
      else:
        savegameresult = savegame.load(username, password)
        if savegameresult == "FILE":
          print("that saved gamed does not exist")
          wait()
          action = None
          savegameresult = None
        elif savegameresult == "PASS":
          print("incorrect password for saved game")
          wait()
          action = None
          savegameresult = None
        else:
          action = "continue"
    elif menuinput == "start":
      utils.clear()
      print(" Create a New Saved Game")
      print("=========================")
      username = input("saved game name: ")
      password = input("password: ")
      if username == "":
        action = None
        savegameresult = None
      else:
        savegameresult = savegame.create(username, password, overwrite=False)
        if savegameresult == "NA":
          action = None
          savegameresult = None
        else:
          action = "continue"
    elif menuinput == "tutorial":
      tutorial.run()
      action = None
    elif menuinput == "exit":
      sys.exit(0)
    else:
      action = None

  game(savegameresult, items, npcs, world, quests, containers, [username, password])

def wrapprint(text, charlength):
  cnt = 0
  newouttext = ""
  
  for currchar in text:
    
    if cnt == charlength:
      if currchar == " ":
        newouttext += "\n"
        cnt = 0
      else:
        newouttext += currchar
    else:
      cnt += 1
      newouttext += currchar

  return newouttext

def game(player, items, npcs, world, quests, containers, userdata):
  lastlocation = ""

  while True:
    utils.clear()
    cr = world[player["location"]]

    # this will let npcs stay there, but will cause unwanted side effects
    # such as not being able to update the current player npcs
    #if lastlocation != player["location"]:
    currentnpcs = utils.npcs(player, npcs)

    lastlocation = player["location"]
  
    player["moves"] += 1

    if player["moves"] % 5 == 0:
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

    newouttext = wrapprint(utils.replaceinstrings(outtext, player), 70)
        
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
      print("Are you sure you want to exit? Make sure to save first")
      if utils.prompt():
        return # exit gameloop
    elif command[0] == "NAC":
      utils.typing("unknown command", player)
      wait()
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
        wait()
    elif command[0] == "inventory":
      inventory(player, cr, containers, items)
    elif command[0] == "unlock":
      if "container" in cr:
        unlockchest(player, cr, containers, items)
      else:
        utils.typing("There is nothing to open here", player)
        wait()
    elif command[0] == "talk":
      if command[1] == None:
        if len(currentnpcs) != 0:
          # maybe implement a better way to do multi npc
          utils.typing("Be more specific with who to talk to", player)
          wait()
        else:
          utils.typing("There is noone to talk to", player)
          wait()
      else:
        dialouge(currentnpcs[command[1]], player, quests)
    elif command[0] == "save":
      utils.clear()
      # userdata: username, password
      savegame.save(userdata[0], userdata[1], player)
      utils.typing("Game Saved", player, speed=.1)
      wait()
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
          storemenu(player, items, storedict)
        else:
          utils.typing("The store seems to be closed", player)
          wait()
      else:
        utils.typing("There is not store here", player)
        wait()

if __name__ == "__main__":
  startmenu()