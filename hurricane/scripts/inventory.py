import hurricane.menu as menu
import hurricane.utils as utils
import hurricane.scripts as scripts

import copy
import math

def itemproperties(item, items, player):
  itemprop = items[item]
  if itemprop["value"] <= 1:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth almost nothing", player)
  else:
    utils.typing("On closer examination, it appears to be " + itemprop["desc"] + ". Worth maybe " + str(itemprop["value"]) + " stars.", player)
  utils.wait()

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

    if invMenu.value == False: # if the inventory is empty
      done = True
    else:
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