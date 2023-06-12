import hurricane.menu as menu
import hurricane.utils as utils
import hurricane.scripts as scripts

import copy
import math

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