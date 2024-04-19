from hurricane.const import VERSION

import hurricane.data.tutorial as tutorial
import hurricane.terminal as terminal
import hurricane.savegame as savegame
import hurricane.game as game
import hurricane.utils as utils
import hurricane.menu as menu

import lzma
import json
import sys
import os

def startmenu(assets):
  print("Loading Assets...")
  term = terminal.Terminal()
  
  items = assets["items"]
  npcs = assets["npcs"]
  world = assets["world"]
  quests = assets["quests"]
  containers = assets["containers"]

  rungame = False
  while not rungame:
    menu_str = """ Hurricane - """ + VERSION + """
===================
use wasd or arrow keys to navigate menus

'{saves}' ...... load or create saved games
'{tutorial}' ... start a short tutorial
'{exit}' ....... exit the game"""
    main_menu = menu.menu(menu_str, [["saves", "tutorial", "exit"]])
    
    while main_menu.value == None:
      utils.clear()
      print(main_menu.get())
      keypress = utils.getch(term)
      main_menu.registerkey(keypress)
    
    if main_menu.value == "saves":
      print("Loading Saves...")
      loaded_saves = savegame.get_all_saves()
      load_menu_str = " Savegame Manager\n==================\n"
      load_menu_str += "{new}      {back}\n\n"

      cnt = 1
      for saves in loaded_saves:
        load_menu_str += str(cnt) + ". {" + saves[0] + "}\n"
        cnt += 1

      rungame = False
      load_save_menu = menu.menu(load_menu_str, 
          [["new"] + [x[0] for x in loaded_saves], ["back"]], 
          [["New Game"] + ["Load '" + x[1].title() + "'" for x in loaded_saves], ["Back"]])
      
      while load_save_menu.value == None:
        utils.clear()
        print(load_save_menu.get())
        keypress = utils.getch(term)
        load_save_menu.registerkey(keypress)
        
      if load_save_menu.value == "new":
        save_game_name = terminal.cinput(term, "new save game name: ")
        if save_game_name is None:
          rungame = False
          continue

        save_game_name = save_game_name.lower()          
        if save_game_name in [x[1] for x in loaded_saves]:
          if not utils.prompt(term, "save game already in use, overwrite? "):
            # if no overwrite is wanted
            rungame = False
            continue
        
        password = terminal.cinput(term, "save game password: ")
        if password is None:
          rungame = False
          continue

        new_file_path = savegame.create(save_game_name, password)
        save_game_manager = savegame.SaveMngr(new_file_path, password)
        save_game_manager.load()
        
      elif load_save_menu.value == "back":
        rungame = False
        continue
      else:
        password = terminal.cinput(term, "password: ")
        if password is None:
          rungame = False
          continue
        
        save_game_manager = savegame.SaveMngr(load_save_menu.value, password)
        correct_passwd = save_game_manager.load()
        if correct_passwd:
          rungame = True
          break
        else:
          print("password incorrect")
          rungame = False
          continue

    elif main_menu.value == "tutorial":
      tutorial.run()
      rungame = False
      continue
    elif main_menu.value == "exit":
      sys.exit(0)
    else:
      rungame = False
      continue

  game.Game(save_game_manager, term, items, npcs, world, quests, containers)

if __name__ == "__main__":
  asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/assets.dat")

  with lzma.open(asset_path) as f:
    assets = json.loads(f.read().decode("utf-8"))
    
  startmenu(assets)