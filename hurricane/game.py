import hurricane.menu as menu
import hurricane.cmds as cmds
import hurricane.utils as utils
import hurricane.scripts as scripts
import hurricane.savegame as savegame
import hurricane.data.colors as colors

from hurricane.const import EXIT_KEYS

import copy

class Game(object):
  def __init__(self, save_game_result, screen, items, npcs, world, quests, containers):
    self.savemngr = save_game_result
    self.player = self.savemngr.data
    self.screen = screen
    self.items = items
    self.npcs = npcs
    self.world = world
    self.quests = quests
    self.containers = containers

    self.c = colors.getcolors()

  def say(self, saylist):
    for i in saylist:
      if utils.parsecondition(i[0], self.player):
        self.screen.typing(i[1], self.player)
        utils.wait()
        return

  def unlockchest(self):
    utils.clear()
    if utils.parsecondition(self.cr["container"]["condition"], self.player):
      if not self.player["location"] in self.player["containers"]:
        self.say(self.cr["container"]["say"])
        container = self.containers[self.player["location"]]
        self.player["containers"][self.player["location"]] = copy.deepcopy(container)
      else: # below may want to be taken out
        self.screen.typing("The chest is already unlocked", self.player)
        utils.wait()
        
      scripts.inventory(self)

  def dostables(self):  
    if len(self.player["stables"]) == 0: # there are no stables to travel to
      print("There are no stables to travel to yet")
      utils.wait()
      return
    
    roomname = self.world[self.player["location"]]["name"]
    menustring = " Use " + roomname + " Stables \n"
    menustring += "==============" + "="*len(roomname) + "\n"
  
    reglist = []
    dislist = []
    
    for stablelocation in self.player["stables"]:
      if stablelocation != self.player["location"]:
        menustring += "Travel to '{" + stablelocation + "}'\n"
        reglist.append(stablelocation)
        dislist.append(self.world[stablelocation]["name"])
      else:
        menustring += "Travel to '" + self.world[stablelocation]["name"] + "' "
        menustring += self.c["green"] + "(HERE)\n" + self.c["reset"]
    
    stableMenu = menu.menu(menustring, [reglist], [dislist])
    keypress = None
  
    stableMenu.find()
    
    while stableMenu.value == None:
      utils.clear()
      print(stableMenu.get())
  
      keypress = self.screen.getchar()
      
      stableMenu.registerkey(keypress)
    
    place = stableMenu.value
    if stableMenu.prev_key in EXIT_KEYS:
      return None # if exited the menu
    elif place == False:
      return None # if nothing was selected
    else:
      utils.clear()
      self.player["location"] = place
      self.screen.typing("Travling to " + self.world[place]["name"], self.player, speed=.3)

  def seequests(self):
    done_quests = ""
    not_quests = ""
    
    if len(self.player["quests"]) > 0:
      for qid in self.player["quests"]:
        # check if the quest is compleated (1 past length of quest list)
        if self.player["quests"][qid] == len(self.quests[qid]["points"]): 
          done_quests += utils.word_wrap(self.quests[qid]["name"] + ": " 
                         + utils.replaceinstrings(self.quests[qid]["done"], self.player)
                         + "\n\n")
        else:
          replaced_string = self.quests[qid]["points"][self.player["quests"][qid]]
          not_quests += utils.word_wrap(self.quests[qid]["name"] + ": " 
                        + utils.replaceinstrings(replaced_string, self.player)
                        + "\n\n")
    else:
      not_quests += "No quests yet, go explore!"
  
    utils.clear()
    print(" Current Quests")
    print("================")
    print(not_quests, end="", flush=True)
  
    if done_quests != "":
      print("")
      print(" Compleated Quests")
      print("===================")
      print(done_quests, end="", flush=True)
    
    utils.wait()

  def loop(self):
    utils.clear()
    self.cr = self.world[self.player["location"]]

    currentnpcs = utils.npcs(self)
  
    self.player["moves"] += 1

    self.savemngr.save()

    if "introtext" in self.cr:
      self.say(self.cr["introtext"])

    if "do" in self.cr:
      for i in self.cr["do"]:
        if utils.parsecondition(i[0], self.player):
          utils.parsedo(i[1], self.player)
          break
  
    if not self.player["location"] in self.player["world"]:
      self.player["world"][self.player["location"]] = []
    
    utils.clear()
    
    print(" " + self.cr["name"])
    print("="*(len(self.cr["name"])+2) + "\n")

    outtext = ""
    outtext += self.cr["desc.long"] + ". "

    if "store" in self.cr:
      if utils.parsecondition(self.cr["store"]["condition"], self.player):
        outtext += self.cr["store"]["desc"] + ". "

    if "stable" in self.cr:
      if not self.player["location"] in self.player["stables"]:
        self.player["stables"].append(self.player["location"])
      outtext += self.cr["stable"] + ". "

    if "container" in self.cr:
      outtext += self.cr["container"]["desc"] + ". "

    for a_npc in currentnpcs:
      for obps in currentnpcs[a_npc][0]["observation"]:
        if utils.parsecondition(obps[0], self.player):
          outtext += obps[1] + ". "
          break

    grounditems = self.player["world"][self.player["location"]]
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
        
      outtext += preface + self.items[grounditems[gitem]]["name"] + postface

    newouttext = utils.word_wrap(utils.replaceinstrings(outtext, self.player))
        
    print(newouttext + "\n")
  
    print("You can go:")
  
    for direction in self.cr["dirs"]:
      dirctn = self.cr["dirs"][direction]
      print("  " + direction.capitalize() + ": " + self.world[dirctn["dest"]]["name"] + " - " 
            + self.world[dirctn["dest"]]["desc.short"]) # add in the locked door
  
    print("")
    
    userinput = input(": ")

    command = cmds.parse(userinput, self.player, currentnpcs)

    if command[0] == "EXT":
      utils.clear()
      if self.screen.prompt("Are you sure you want to exit?"):
        return # exit gameloop
    elif command[0] == "NAC":
      self.screen.typing("unknown command", self.player)
      utils.wait()
    elif command[0] == "go":
      print()
      if command[1] in self.cr["dirs"]:
        dr = self.cr["dirs"][command[1]]
        if utils.parsecondition(dr["condition"], self.player):
          self.say(dr["say"])
          utils.parsedo(dr["do"], self.player)
          self.player["location"] = dr["dest"]
        else:
          self.say(dr["say"])
      else:
        self.screen.typing("You cannot go that way", self.player)
        utils.wait()
    elif command[0] == "inventory":
      scripts.inventory(self)
    elif command[0] == "unlock":
      if "container" in self.cr:
        self.unlockchest()
        # only one chest per room
        # so this will always refer to one chest
      else:
        self.screen.typing("There is nothing to open here", self.player)
        utils.wait()
    elif command[0] == "talk":
      if command[1] == None:
        if len(currentnpcs) != 0:
          # maybe implement a better way to do multi npc
          self.screen.typing("To many options to talk to, be more specific", self.player)
          utils.wait()
        else:
          self.screen.typing("Who are you talking to?", self.player)
          utils.wait()
      else:
        scripts.dialouge(currentnpcs[command[1]], self)
    elif command[0] == "quests":
      self.seequests()
    elif command[0] == "stable":
      self.dostables()
    elif command[0] == "store":
      if "store" in self.cr:
        if utils.parsecondition(self.cr["store"]["condition"], self.player):
          storedict = {
            "pricemultiplier" : self.cr["store"]["multiplier"],
            "items" : []
          }
          for i in self.cr["store"]["items"]:
            if utils.parsecondition(i[0], self.player):
              storedict["items"].append(i[1])
          scripts.storemenu(storedict, self)
        else:
          self.screen.typing("The store seems to be closed", self.player)
          utils.wait()
      else:
        self.screen.typing("There is not store here", self.player)
        utils.wait()