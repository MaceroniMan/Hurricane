import hurricane.data.htf as htf
from hurricane.const import SAVE_FOLDER_NAME
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

class SaveMngr(object):
  def __init__(self, save_file_path, password):
    self.save_file_path = save_file_path
    self.password = password
    self.dta = {}

  def load(self):
    with open(self.save_file_path, "rb") as file:
      file_data = file.read()
    
    self.dta = json.loads(htf.decode(file_data[4:], self.password))

  def save(self):
    save_file_data = htf.encode(json.dumps(self.dta), self.password)
    with open(self.save_file_path, "wb") as file:
      file.write(b"HGSF")
      file.write(save_file_data)
    
def get_all_saves():
  cur_path = os.getcwd()
  print(cur_path)
  save_folder_path = os.path.join(cur_path, SAVE_FOLDER_NAME)
  if not os.path.exists(save_folder_path): # make sure directory exists
    os.mkdir(save_folder_path)
  
  save_files = []
  for file_path in os.listdir(save_folder_path):
    full_file_path = os.path.join(save_folder_path, file_path)
    if os.path.isfile(full_file_path):
      with open(full_file_path, "rb") as file:
        start_bytes = file.read(4)
        if start_bytes == b'HGSF': # check to validate its a correct file
          save_files.append((full_file_path, file_path))
  
  return save_files
  
def get_path(save_file_name):
  cur_path = os.getcwd()
  save_path = os.path.join(cur_path, SAVE_FOLDER_NAME)
  if not os.path.exists(save_path):
    os.mkdir(save_path)
  return os.path.join(save_path, save_file_name)

def create(save_file_name, password):
  new_save_path = get_path(save_file_name)

  newplayer = BASEPLAYER.copy()
  newplayer["name"] = input("charecter name? ").title()

  return new_save_path