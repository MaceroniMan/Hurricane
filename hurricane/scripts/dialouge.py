import hurricane.menu as menu
import hurricane.utils as utils
import hurricane.const as const

def dialouge(npc, game):
  dialougedict = npc[0]["dialouges"]
  talklocation = npc[1]
  starttext = ""
  prev = None

  while True:
    print(game.screen.clear, end="")
    
    if not talklocation in dialougedict:
      raise ValueError(talklocation + " does not exist")
      
    dialougecurrent = dialougedict[talklocation]
    beforetext = ""

    if starttext != "":
      beforetext += starttext + "\n\n"
    
    # if the user asked a question
    if prev == None:
      dialouges = dialougecurrent["dialouge"]
    else:
      dialouges = [prev] + dialougecurrent["dialouge"]

    prev = None
    
    for person_index in range(len(dialouges)):
      print(game.screen.clear, end="")
      print(utils.replace_in_strings(beforetext, game.player, game.screen), end="", flush=True)
      
      person = dialouges[person_index]
      text = utils.word_wrap('  "' + person[1].replace("`", '"`  "') + '"', "`", "\n   ")
      print(person[0] + ": ", end="\n", flush=True)
      doneskip = game.screen.typing(text, game.player)
      if doneskip:
        print(game.screen.clear, end="")
        print(utils.replace_in_strings(beforetext, game.player, game.screen), end="", flush=True)
        print(person[0] + ": \n"
              + utils.replace_in_strings(text, game.player, game.screen).replace("`", "\n"),
              end="", flush=True)
      
      beforetext += person[0] + ": \n" + text.replace("`", "\n") + "\n\n"
      if person_index+1 != len(dialouges):
        input()
      
    doext = utils.parsedo(dialougecurrent["do"], game.player)

    if doext == "EXT":
      input()
      break # end the dialouge menu
    elif doext != "NA":
      input() # add a extra pause in flow
      print(game.screen.clear, end="")
      if game.player["quests"][doext] == 0: # if the quest was just given
        game.screen.typing("Quest '" + game.quests[doext]["name"] + "' received", game.player, speed=.1)
      # if the quest was just compleated (1 past length of quest list)
      elif game.player["quests"][doext] == len(game.quests[doext]["points"]): 
        game.screen.typing("Quest '" + game.quests[doext]["name"] + "' compleated", game.player, speed=.1)
      else:
        game.screen.typing("Quest '" + game.quests[doext]["name"] + "' advanced", game.player, speed=.1)
      utils.wait()
    
    if len(dialougecurrent["options"]) == 0:
      input()
      break
    else:
      optionstring = ""
      nicelist = [[]]
      optionlist = [[]]
    
      for option in dialougecurrent["options"]:
        if utils.parsecondition(option[0], game.player):
          # added the dollar sign so that if two options went to the same place
          # they would still be different selections
          optionstring += "{" + option[1]["goto"] + "$" + option[1]["text"] + "}\n"
          nicelist[0].append(option[1]["text"])
          optionlist[0].append(option[1]["goto"] + "$" + option[1]["text"])

      beforetext = utils.replace_in_strings(beforetext, game.player, game.screen)
      beforetext = beforetext.replace("`", "\n")
      dialoueMenu = menu.menu(beforetext + optionstring, game.screen, optionlist, nicelist)

      with game.screen.hidden_cursor():
        while dialoueMenu.value == None:
          print(game.screen.clear + dialoueMenu.get())
  
          keypress = game.screen.getchar()
  
          dialoueMenu.registerkey(keypress, menu.layouts.NOESC)

      talklocation = dialoueMenu.value.split("$")[0]

      # find the dialouge to put the question asked by user at top
      prev = ["You", dialoueMenu.niceValue]

    if talklocation == "exit":
      break # leave the menu