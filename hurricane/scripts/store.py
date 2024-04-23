import hurricane.menu as menu
import hurricane.utils as utils

from hurricane.const import EXIT_KEYS

import copy
import math

"""
Store Dict:
{
  "pricemultiplier" : 0
  "name" : []
}
"""

def storemenu(storedict, game):
  print(game.screen.clear, end="")

  done = False

  buyback = []

  while not done:
    maxinvlength = 9
    for i in game.player["inventory"]:
      nme = game.items[i]["name"]
      if len(nme) > maxinvlength:
        maxinvlength = len(nme)
    
    maxstolength = 5
    for i in storedict["items"]:
      nme = game.items[i]["name"]
      if len(nme) > maxstolength:
        maxstolength = len(nme)

    maxbuylength = 7
    for i in buyback:
      nme = game.items[i]["name"]
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

    printstring = "Stars: " + str(game.player["stars"]) + "\n\n"

    reglist_inv = []
    reglist_sto = []
    reglist_buy = []

    dislist_inv = []
    dislist_sto = []
    dislist_buy = []
    
    printstring += "+-" + "-"*math.ceil(inventorytitleminus/2) + "inventory" + "-"*math.ceil(inventorytitleminus/2) + "-+-" + "-"*math.ceil(storetitleminus/2) + "store" + "-"*math.ceil(storetitleminus/2) + "-+-" + "-"*math.ceil(buybacktitleminus/2) + "buyback" + "-"*math.ceil(buybacktitleminus/2) + "-+" + "\n"

    maxlength = max([len(storedict["items"]), len(game.player["inventory"]), len(buyback)])+1

    printstring += "| " + " "*(maxinvlength) + " | " + " "*(maxstolength) + " | " + " "*(maxbuylength) + " |\n"

    for i in range(maxlength):
      if i < len(game.player["inventory"]):
        extraspaces = maxinvlength-len(game.items[game.player["inventory"][i]]["name"])
        printstring += "| " + " "*(extraspaces) + "{inv$" + game.player["inventory"][i] + "$" + str(i) + "} |"
        dislist_inv.append(game.items[game.player["inventory"][i]]["name"])
        reglist_inv.append("inv$" + game.player["inventory"][i] + "$" + str(i))
      else:
        printstring += "| " + " "*(maxinvlength) + " |"


      if i < len(storedict["items"]):
        extraspaces = maxstolength-len(game.items[storedict["items"][i]]["name"])
        printstring += " " + " "*(extraspaces) + "{sto$" + storedict["items"][i] + "$" + str(i) + "} |"
        dislist_sto.append(game.items[storedict["items"][i]]["name"])
        reglist_sto.append("sto$" + storedict["items"][i] + "$" + str(i))
      else:
        printstring += " " + " "*(maxstolength) + " |"

      if i < len(buyback):
        extraspaces = maxbuylength-len(game.items[buyback[i]]["name"])
        printstring += " " + " "*(extraspaces) + "{buy$" + buyback[i] + "$" + str(i) + "} |"
        dislist_buy.append(game.items[buyback[i]]["name"])
        reglist_buy.append("buy$" + buyback[i] + "$" + str(i))
      else:
        printstring += " " + " "*(maxbuylength) + " |"
  
      printstring += "\n" # end the line

    printstring += "+-" + "-"*(maxinvlength) + "-+-" + "-"*(maxstolength) + "-+-" + "-"*(maxbuylength) + "-+\n"
    
    invMenu = menu.menu(printstring, game.screen, [reglist_inv, reglist_sto, reglist_buy], [dislist_inv, dislist_sto, dislist_buy])
    invMenu.find()

    with game.screen.hidden_cursor():
      while invMenu.value == None:
        print(game.screen.clear + invMenu.get())
  
        keypress = game.screen.getchar()
        
        invMenu.registerkey(keypress)

    item = invMenu.value.split("$")
    if invMenu.prev_key in EXIT_KEYS:
      done = True
    else:
      if item[0] == "sto":
        stars = game.items[item[1]]["value"] * storedict["pricemultiplier"]
        pr_text = "Do you want to purchase a " + item[1] + " for " + str(stars) + " stars?"
        if game.screen.prompt(pr_text):
          if stars > game.player["stars"]:
            print("You do not have enough stars!")
          else:
            game.player["stars"] -= stars
            game.player["inventory"].append(item[1])
            print("You purchased a " + item[1] + " for " + str(stars) + " stars")
      elif item[0] == "inv":
        stars = game.items[item[1]]["value"]
        pr_text = "Do you want to sell a " + item[1] + " for " + str(stars) + " stars?"
        if game.screen.prompt(pr_text):
          print("You sold a " + item[1] + " for " + str(stars) + " stars")
          game.player["stars"] += stars
          game.player["inventory"].remove(item[1])
          buyback.append(item[1])
      elif item[0] == "buy":
        stars = game.items[item[1]]["value"]
        pr_text = "Do you want to purchase a " + item[1] + " for " + str(stars) + " stars?"
        if game.screen.prompt(pr_text):
          if stars > game.player["stars"]:
            print("You do not have enough stars!")
          else:
            game.player["stars"] -= stars
            game.player["inventory"].append(item[1])
            buyback.remove(item[1])
            print("You purchased a " + item[1] + " for " + str(stars) + " stars")