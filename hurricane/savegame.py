import hurricane.data.htf as htf
import json
import os

BASEPLAYER = {
  "name" : "", # the current player name
  "stars" : 0, # their version of money
  "moves" : 0, # the total count of the moves
  "location" : "z1-docks", # the current player location
  "flags" : {}, # game flags
  "inventory" : [], # the inventory of all the items the player has on them
  "quests" : {}, # a list of all the quests and the progress on them ex. "z1-main": 0
  "stables" : [], # a list of all the places you can 'teleport' to
  "world" : {}, # a way to save what items have been dropped on the ground
  "containers" : {}, # a way to save the state of the containers in the world
  "recipes" : [] # a list of all the current crafting recipies
}

def getPath(username):
  cur_path = os.getcwd()
  save_path = os.path.join(cur_path, "saves")
  if not os.path.exists(save_path):
    os.mkdir(save_path)
  return os.path.join(save_path, username)

def load(username, password):
  username = username.lower()
  savepath = getPath(username)
  if os.path.exists(savepath):
    try:
      return json.loads(htf.decode(savepath, password))
    except TypeError:
      return "PASS"
  else:
    return "FILE"

def create(username, password, overwrite=False):
  username = username.lower()
  savepath = getPath(username)
  if os.path.exists(savepath) and overwrite:
    if input("this saved game already exists, overwrite? [yes/no] ") != "yes":
      return "NA"

  newplayer = BASEPLAYER.copy()

  newplayer["name"] = input("charecter name? ").title()
  
  htf.encode(json.dumps(newplayer), password, savepath)

  return newplayer

def save(username, password, player):
  username = username.lower()
  htf.encode(json.dumps(player), password, getPath(username))