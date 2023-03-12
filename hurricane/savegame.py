import data.htf as htf
import json
import os
import utils

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

def load(username, password):
  savepath = "saves/" + username
  if os.path.exists(savepath):
    try:
      return json.loads(htf.decode(savepath, password))
    except TypeError:
      return "PASS"
  else:
    return "FILE"

def create(username, password, overwrite=False):
  savepath = "saves/" + username
  if os.path.exists(savepath) and overwrite:
    if input("this saved game already exists, overwrite? [yes/no] ") != "yes":
      return "NA"

  newplayer = BASEPLAYER.copy()

  utils.clear()
  print(" Charecter Creation")
  print("====================")
  newplayer["name"] = input("charecter name? ")
  
  htf.encode(json.dumps(newplayer), password, "saves/" + username)

  return newplayer

def save(username, password, player):
  htf.encode(json.dumps(player), password, "saves/" + username)