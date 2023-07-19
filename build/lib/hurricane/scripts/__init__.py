import hurricane.scripts.dialouge as short_dialouge
import hurricane.scripts.inventory as short_inventory
import hurricane.scripts.store as short_store
import hurricane.scripts.crafting as short_crafting

# make it easier to call script functions
def inventory(player, room, containers, items):
  short_inventory.inventory(player, room, containers, items)

def store(player, items, storedict):
  short_store.store(player, items, storedict)

def dialouge(npc, player, quests):
  short_dialouge.dialouge(npc, player, quests)

def craft(player, items, cr, world):
  short_crafting.craft(player, items, cr, world)