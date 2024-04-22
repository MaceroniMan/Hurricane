import hurricane.menu as menu
import hurricane.utils as utils
from hurricane.const import EXIT_KEYS, ENTER_KEYS

import copy
import math

def itemproperties(item, game):
  itemprop = game.items[item]
  if itemprop["value"] <= 1:
    game.screen.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth almost nothing", game.player)
  else:
    game.screen.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth maybe " + str(itemprop["value"]) + " stars.", game.player)
  utils.wait()

def inventory(game):
  # note: bag is the same as containers and chests
  utils.clear()

  done = False
  
  while not done:
    maxinvlength = 9
    for i in game.player["inventory"]:
      nme = game.items[i]["name"]
      if len(nme) > maxinvlength:
        maxinvlength = len(nme)

    maxgndlength = 6
    grounditems = copy.deepcopy(game.player["world"][game.player["location"]])
    for i in grounditems:
      nme = game.items[i]["name"]
      if len(nme) > maxgndlength:
        maxgndlength = len(nme)
  
    maxbaglength = None
    currentcontainer = []

    if "container" in game.cr:
      if utils.parsecondition(game.cr["container"]["condition"], game.player):
        if game.player["location"] in game.player["containers"]:
          currentcontainer = copy.deepcopy(game.player["containers"][game.player["location"]])
          
          maxbaglength = 5
          
          for i in currentcontainer:
            nme = game.items[i]["name"]
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
  
    printstring = "Stars: " + str(game.player["stars"]) + "\n\n"
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
  
    maxlength = max([len(currentcontainer), len(game.player["inventory"]), len(grounditems)])+1
  
    printstring += "| " + " "*(maxinvlength) + " |"
    if maxbaglength != None:
      printstring += " " + " "*(maxbaglength) + " |"
    printstring += " " + " "*(maxgndlength) + " |"
    printstring += "\n" # end the line
    
    for i in range(maxlength):
      if i < len(game.player["inventory"]):
        extraspaces = maxinvlength-len(game.items[game.player["inventory"][i]]["name"])
        
        printstring += "| " + " "*(extraspaces) + "{inv$" + game.player["inventory"][i] + "$" + str(i) + "} |"
        dislist_inv.append(game.items[game.player["inventory"][i]]["name"])
        reglist_inv.append("inv$" + game.player["inventory"][i] + "$" + str(i))
      else:
        printstring += "| " + " "*(maxinvlength) + " |"

      if i < len(currentcontainer):
        extraspaces = maxbaglength-len(game.items[currentcontainer[i]]["name"])
        
        printstring += " " + " "*(extraspaces) + "{bag$" + currentcontainer[i] + "$" + str(i) + "} |"
        dislist_bag.append(game.items[currentcontainer[i]]["name"])
        reglist_bag.append("bag$" + currentcontainer[i] + "$" + str(i))
      elif maxbaglength != None:
        printstring += " " + " "*(maxbaglength) + " |"

      if i < len(grounditems):
        extraspaces = maxgndlength-len(game.items[grounditems[i]]["name"])

        printstring += " " + " "*(extraspaces) + "{gnd$" + grounditems[i] + "$" + str(i) + "} |"
        dislist_gnd.append(game.items[grounditems[i]]["name"])
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

    
    inv_menu = menu.menu(printstring, reglist, dislist)
    keypress = None

    inv_menu.find()

    currentoutputmenu = ""
    
    while inv_menu.value == None:
      utils.clear()
      currentoutputmenu = inv_menu.get()
      print(currentoutputmenu)

      keypress = game.screen.getchar()
      
      inv_menu.registerkey(keypress)

    if inv_menu.value == False: # if the inventory is empty
      done = True
    elif inv_menu.prev_key in EXIT_KEYS:
      done = True
    elif inv_meni.prev_key in ENTER_KEYS:
      item = inv_menu.value.split("$")
      itemproperties(item[1], game)
    elif inv_menu.prev_key == " ":
      item = inv_menu.value.split("$")
      movedone = False
      while not movedone:
        movedone = True # will set as false when moving items is done

        currentoutputmenu = currentoutputmenu.replace("-inventory-", "-{inventory}-").replace("-chest-", "-{chest}-").replace("-ground-", "-{ground}-")

        currentoutputmenu += "Where to move " + game.items[item[1]]["name"] + "?"

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

          keypress = game.screen.getchar()
      
          moveMenu.registerkey(keypress)
        
        if moveMenu.value == "inventory":
          if item[0] == "gnd":
            game.player["inventory"].append(item[1])
            game.player["world"][game.player["location"]].remove(item[1])
          elif item[0] == "bag":
            game.player["inventory"].append(item[1])
            game.player["containers"][game.player["location"]].remove(item[1])
        elif moveMenu.value == "chest":
          if maxbaglength != None:
            if item[0] == "inv":
              game.player["containers"][game.player["location"]].append(item[1])
              game.player["inventory"].remove(item[1])
            elif item[0] == "gnd":
              game.player["containers"][game.player["location"]].append(item[1])
              game.player["world"][game.player["location"]].remove(item[1])
        elif moveMenu.value == "ground":
          if item[0] == "inv":
            game.player["world"][game.player["location"]].append(item[1])
            game.player["inventory"].remove(item[1])
          elif item[0] == "bag":
            game.player["world"][game.player["location"]].append(item[1])
            game.player["containers"][game.player["location"]].remove(item[1])