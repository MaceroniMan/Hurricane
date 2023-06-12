import hurricane.cmds as cmds
import hurricane.utils as utils
import hurricane.const as const

def run():
  utils.clear()
  utils.typing(utils.wrapprint("Hello and welcome to Hurricane! This is a short-interactive tutorial to show you all of the commands that can be run! Use the 'enter' key to continue when '...' shows up.", const.WIDTH))
  utils.wait()

  utils.typing(utils.wrapprint("Nice! Next up is moving. Hurricane is pretty good at knowing what you want to do, so just type 'go north' or even just 'north'.", const.WIDTH))
  done = False
  while not done:
    out = cmds.parse(input(": "), {}, [])
    if out[0] == "go":
      done = True
      if out[1] != "north":
        utils.typing("Close enough, but your goal was to go 'north'...")
      else:
        utils.typing("Nice job! Onto the next command.")
    else:
      utils.typing("Nope! Try again.")

  utils.wait()
  utils.clear()
  utils.typing(utils.wrapprint("Next is the 'talk' command. Use it when you want to interact with a NPC. When there is more than one NPC in the current room make sure to specify the NPC you want to talk too. As practice, talk to 'Fred' over there.", const.WIDTH))

  done = False
  while not done:
    out = cmds.parse(input(": "), {}, [["Fred"]])
    if out[0] == "talk":
      done = True
      utils.typing("Nice job! Onto the next command.")
    else:
      utils.typing("Nope! Try again.")

  utils.wait()
  utils.clear()
  utils.typing("Lastly are the more simple commands;` - 'bag' for the inventory` - 'open' or 'look' to look into a container` - 'store' to view the store interface if there is one` - 'quest' to view the current questing status` - 'travel' or 'stable' to view the teleport menu when in a stable` - 'exit' to exit the game")

  utils.wait()
  utils.clear()
  utils.typing(utils.wrapprint("Congradulations! You have finished the tutorial, go have fun!", const.WIDTH))
  utils.wait()

  return