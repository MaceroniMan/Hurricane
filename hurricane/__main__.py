from hurricane.const import VERSION, EXIT_KEYS

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
  screen = terminal.Terminal()
  
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
    main_menu = menu.menu(menu_str, screen, [["saves", "tutorial", "exit"]])
    
    with screen.hidden_cursor():
      while main_menu.value == None:
        print(screen.clear, main_menu.get())
        keypress = screen.getchar()
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
      load_save_menu = menu.menu(load_menu_str, screen,
          [["new"] + [x[0] for x in loaded_saves], ["back"]], 
          [["New Game"] + ["Load '" + x[1].title() + "'" for x in loaded_saves], ["Back"]])

      with screen.hidden_cursor():
        while load_save_menu.value == None:
          print(screen.clear, load_save_menu.get())
          keypress = screen.getchar()
          load_save_menu.registerkey(keypress)

      if load_save_menu.prev_key in EXIT_KEYS:
        rungame = False
        continue
      if load_save_menu.value == "new":
        save_game_name = screen.cinput("new save game name: ")
        if save_game_name is None:
          rungame = False
          continue

        save_game_name = save_game_name.lower()          
        if save_game_name in [x[1] for x in loaded_saves]:
          if not screen.prompt("save game already in use, overwrite? "):
            # if no overwrite is wanted
            rungame = False
            continue
        
        password = screen.cinput("save game password: ")
        if password is None:
          rungame = False
          continue

        new_save_path = savegame.get_path(save_game_name)
        save_game_manager = savegame.SaveMngr(new_save_path, password)
        save_game_manager.reset()
        save_game_manager.save()
        rungame = True
        continue
      elif load_save_menu.value == "back":
        rungame = False
        continue
      else:
        password = screen.cinput("password: ")
        if password is None:
          rungame = False
          continue
        
        save_game_manager = savegame.SaveMngr(load_save_menu.value, password)
        correct_passwd = save_game_manager.load()
        if correct_passwd:
          rungame = True
          continue
        else:
          print("password incorrect")
          utils.wait()
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

  game_class = game.Game(save_game_manager,
                         screen,
                         items,
                         npcs,
                         world,
                         quests,
                         containers)

  while True:
    game_class.loop()

if __name__ == "__main__":
  asset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/assets.dat")

  with lzma.open(asset_path) as f:
    assets = json.loads(f.read().decode("utf-8"))
    
  startmenu(assets)