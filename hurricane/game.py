import hurricane.menu as menu
import hurricane.cmds as cmds
import hurricane.utils as utils
import hurricane.const as const
import hurricane.savegame as savegame
import hurricane.data.colors as colors

import copy
import math

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
  c = colors.getcolors()

  if len(player["stables"]) == 0: # there are no stables to travel to
    print("There are no stables to travel to yet")
    wait()
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
  
  wait()

def dialouge(npc, player, quests):
  dialougedict = npc[0]["dialouges"]
  talklocation = npc[1]
  starttext = ""
  prev = None

  while True:
    utils.clear()
    
    if not talklocation in dialougedict:
      raise ValueError(talklocation + " does not exist")
      
    dialougecurrent = dialougedict[talklocation]
    beforetext = ""

    if starttext != "":
      beforetext += starttext + "\n\n"
    
    # if the user asked a question
    if prev == None:
      dialouges = dialougecurrent["dialouge"]
    else:
      dialouges = [prev] + dialougecurrent["dialouge"]

    prev = None
    
    for person_index in range(len(dialouges)):
      utils.clear()
      print(utils.replaceinstrings(beforetext, player), end="", flush=True)
      
      person = dialouges[person_index]
      text = utils.wrapprint('  "' + person[1].replace("`", '"`  "') + '"', const.WIDTH, "`", "\n   ")
      print(person[0] + ": ", end="\n", flush=True)
      doneskip = utils.typing(text, player)
      if doneskip:
        utils.clear()
        print(utils.replaceinstrings(beforetext, player), end="", flush=True)
        print(person[0] + ": \n" + utils.replaceinstrings(text, player).replace("`", "\n"), end="", flush=True)
      
      beforetext += person[0] + ": \n" + text.replace("`", "\n") + "\n\n"
      if person_index+1 != len(dialouges):
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

      # find the dialouge to put the question asked by user at top
      prev = ["You", dialoueMenu.niceValue]

    if talklocation == "exit":
      break # leave the menu

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
          utils.typing("To many options to talk to, be more specific", player)
          wait()
        else:
          utils.typing("Who are you talking to?", player)
          wait()
      else:
        dialouge(currentnpcs[command[1]], player, quests)
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