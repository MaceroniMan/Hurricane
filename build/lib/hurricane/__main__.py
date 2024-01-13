from hurricane.const import KEY, VERSION

import hurricane.data.tutorial as tutorial
import hurricane.data.htf as htf
import hurricane.savegame as savegame
import hurricane.game as game
import hurricane.utils as utils
import hurricane.menu as menu

import json
import sys
import os

def startmenu():
  print("Loading Assets...")
  asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/assets.dat")
  
  assets = json.loads(htf.decode(asset_path, KEY))
  items = assets["items"]
  npcs = assets["npcs"]
  world = assets["world"]
  quests = assets["quests"]
  containers = assets["containers"]

  action = None
  savegameresult = ""
  while action == None:
    menustr = """ Hurricane - """ + VERSION + """
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
          utils.wait()
          action = None
          savegameresult = None
        elif savegameresult == "PASS":
          print("incorrect password for saved game")
          utils.wait()
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

  game.game(savegameresult, items, npcs, world, quests, containers, [username, password])

if __name__ == "__main__":
  startmenu()