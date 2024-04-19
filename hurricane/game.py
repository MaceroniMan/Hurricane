import hurricane.menu as menu
import hurricane.cmds as cmds
import hurricane.utils as utils
import hurricane.const as const
import hurricane.scripts as scripts
import hurricane.savegame as savegame
import hurricane.data.colors as colors

import copy

class Game(object):
  def __init__(self, save_game_result, term, items, npcs, world, quests, containers):
    self.pmgr = save_game_result
    self.term = term
    self.items = items
    self.npcs = npcs
    self.world = world
    self.quests = quests
    self.containers = containers

    self.c = colors.getcolors()

    while True:
      self.loop()

  def say(self, saylist):
    for i in saylist:
      if utils.parsecondition(i[0], self.pmgr.data):
        utils.typing(i[1], self.term, self.pmgr.data)
        utils.wait()
        return

  def unlockchest(self):
    utils.clear()
    if utils.parsecondition(self.cr["container"]["condition"], self.pmgr.data):
      if not self.pmgr.data["location"] in self.pmgr.data["containers"]:
        self.say(self.cr["container"]["say"])
        container = self.containers[self.pmgr.data["location"]]
        self.pmgr.data["containers"][self.pmgr.data["location"]] = copy.deepcopy(container)
      else: # below may want to be taken out
        utils.typing("The chest is already unlocked", self.pmgr.data)
        utils.wait()
        
      scripts.inventory(self)

  def dostables(self):  
    if len(self.pmgr.data["stables"]) == 0: # there are no stables to travel to
      print("There are no stables to travel to yet")
      utils.wait()
      return
    
    roomname = self.world[self.pmgr.data["location"]]["name"]
    menustring = " Use " + roomname + " Stables \n"
    menustring += "==============" + "="*len(roomname) + "\n"
  
    reglist = []
    dislist = []
    
    for stablelocation in self.pmgr.data["stables"]:
      if stablelocation != self.pmgr.data["location"]:
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
  
      keypress = utils.getch(self.term)
      
      stableMenu.registerkey(keypress)
    
    place = stableMenu.value
    if keypress == "`":
      return None # if exited the menu
    elif place == False:
      return None # if nothing was selected
    else:
      utils.clear()
      self.pmgr.data["location"] = place
      utils.typing("Travling to " + self.world[place]["name"], self.term, self.pmgr.data, speed=.3)

  def seequests(self):
    done_quests = ""
    not_quests = ""
    
    if len(self.pmgr.data["quests"]) > 0:
      for qid in self.pmgr.data["quests"]:
        # check if the quest is compleated (1 past length of quest list)
        if self.pmgr.data["quests"][qid] == len(self.quests[qid]["points"]): 
          done_quests += utils.wrapprint(self.quests[qid]["name"] + ": " 
                         + utils.replaceinstrings(self.quests[qid]["done"], self.pmgr.data)
                         + "\n\n", const.WIDTH)
        else:
          replaced_string = self.quests[qid]["points"][self.pmgr.data["quests"][qid]]
          not_quests += utils.wrapprint(self.quests[qid]["name"] + ": " 
                        + utils.replaceinstrings(replaced_string, self.pmgr.data)
                        + "\n\n", const.WIDTH)
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
    self.cr = self.world[self.pmgr.data["location"]]

    currentnpcs = utils.npcs(self)
  
    self.pmgr.data["moves"] += 1

    savegame.save(self.userdata[0], self.userdata[1], self.pmgr.data)

    if "introtext" in self.cr:
      self.say(self.cr["introtext"])

    if "do" in self.cr:
      for i in self.cr["do"]:
        if utils.parsecondition(i[0], self.pmgr.data):
          utils.parsedo(i[1], self.pmgr.data)
          break
  
    if not self.pmgr.data["location"] in self.pmgr.data["world"]:
      self.pmgr.data["world"][self.pmgr.data["location"]] = []
    
    utils.clear()
    
    print(" " + self.cr["name"])
    print("="*(len(self.cr["name"])+2) + "\n")

    outtext = ""
    outtext += self.cr["desc.long"] + ". "

    if "store" in self.cr:
      if utils.parsecondition(self.cr["store"]["condition"], self.pmgr.data):
        outtext += self.cr["store"]["desc"] + ". "

    if "stable" in self.cr:
      if not self.pmgr.data["location"] in self.pmgr.data["stables"]:
        self.pmgr.data["stables"].append(self.pmgr.data["location"])
      outtext += self.cr["stable"] + ". "

    if "container" in self.cr:
      outtext += self.cr["container"]["desc"] + ". "

    for a_npc in currentnpcs:
      for obps in currentnpcs[a_npc][0]["observation"]:
        if utils.parsecondition(obps[0], self.pmgr.data):
          outtext += obps[1] + ". "
          break

    grounditems = self.pmgr.data["world"][self.pmgr.data["location"]]
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

    newouttext = utils.wrapprint(utils.replaceinstrings(outtext, self.pmgr.data), const.WIDTH)
        
    print(newouttext + "\n")
  
    print("You can go:")
  
    for direction in self.cr["dirs"]:
      dirctn = self.cr["dirs"][direction]
      print("  " + direction.capitalize() + ": " + self.world[dirctn["dest"]]["name"] + " - " 
            + self.world[dirctn["dest"]]["desc.short"]) # add in the locked door
  
    print("")
    
    userinput = input(": ")

    command = cmds.parse(userinput, self.pmgr.data, currentnpcs)

    if command[0] == "EXT":
      utils.clear()
      print("Are you sure you want to exit?")
      if utils.prompt(self.term):
        return # exit gameloop
    elif command[0] == "NAC":
      utils.typing("unknown command", self.pmgr.data)
      utils.wait()
    elif command[0] == "go":
      print()
      if command[1] in self.cr["dirs"]:
        dr = self.cr["dirs"][command[1]]
        if utils.parsecondition(dr["condition"], self.pmgr.data):
          self.say(dr["say"])
          utils.parsedo(dr["do"], self.pmgr.data)
          self.pmgr.data["location"] = dr["dest"]
        else:
          self.say(dr["say"])
      else:
        utils.typing("You cannot go that way", self.pmgr.data)
        utils.wait()
    elif command[0] == "inventory":
      scripts.inventory(self)
    elif command[0] == "unlock":
      if "container" in self.cr:
        self.unlockchest()
        # only one chest per room
        # so this will always refer to one chest
      else:
        utils.typing("There is nothing to open here", self.pmgr.data)
        utils.wait()
    elif command[0] == "talk":
      if command[1] == None:
        if len(currentnpcs) != 0:
          # maybe implement a better way to do multi npc
          utils.typing("To many options to talk to, be more specific", self.pmgr.data)
          utils.wait()
        else:
          utils.typing("Who are you talking to?", self.pmgr.data)
          utils.wait()
      else:
        scripts.dialouge(currentnpcs[command[1]], self)
    elif command[0] == "quests":
      self.seequests()
    elif command[0] == "stable":
      self.dostables()
    elif command[0] == "store":
      if "store" in self.cr:
        if utils.parsecondition(self.cr["store"]["condition"], self.pmgr.data):
          storedict = {
            "pricemultiplier" : self.cr["store"]["multiplier"],
            "items" : []
          }
          for i in self.cr["store"]["items"]:
            if utils.parsecondition(i[0], self.pmgr.data):
              storedict["items"].append(i[1])
          scripts.storemenu(storedict, self)
        else:
          utils.typing("The store seems to be closed", self.pmgr.data)
          utils.wait()
      else:
        utils.typing("There is not store here", self.pmgr.data)
        utils.wait()