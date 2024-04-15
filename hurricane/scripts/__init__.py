import hurricane.scripts.dialouge as short_dialouge
import hurricane.scripts.inventory as short_inventory
import hurricane.scripts.store as short_store
import hurricane.scripts.crafting as short_crafting

# make it easier to call script functions
def inventory(game):
  short_inventory.inventory(game)

def store(storedict, game):
  short_store.store(storedict, game)

def dialouge(npc, game):
  short_dialouge.dialouge(npc, game)

def craft(player, items, cr, world):
  short_crafting.craft(player, items, cr, world)