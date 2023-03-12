import hurricane.data.htf as htf
import json

KEY = "hurricane"

# room key explinations:
"""
name: the human readable name of the room
desc.long: the long decription, read when first entering the room
desc.short: a short description of the room
introtext: a list of texts, the first true one will print out to the screen
store: a list of items, all of the true items will be visible in the store
container: a chest of sorts
stable: the description of the stable
"""

world = {
  "z1-docks" : {
    "name" : "Dockyard",
    "desc.long" : "You are in a small dockyard with only two ships docked along the pier, there is also faint smell of salty sea air mixed with seaweed that drifts off the ocean",
    "desc.short" : "A small dockyard",
    "dirs" : {
      "south" : {
        "dest" : "z1-boardwalk",
        "say" : [
          ["not flag('z1.docks.south') and has('dagger')", "[@] used Dagger to cut through vines"],
          ["not flag('z1.docks.south') and not has('dagger')", "There are some spiky vines blocking your way"]
        ],
        "condition" : "has('dagger') or flag('z1.docks.south')",
        "do" : "set z1.docks.south 1"
      }
    },
  },
  "z1-boardwalk" : {
    "name" : "Boardwalk",
    "desc.long" : "A vary old wooden boardwalk with some chunks missing from it, there are large trees that look for the most part like mangrove trees, and there is the faint sound of seabirds",
    "desc.short" : "A old boardwalk",
    "dirs" : {
      "north" : {
        "dest" : "z1-docks",
        "say" : [],
        "condition" : "true",
        "do" : ""
      },
      "south" : {
        "dest" : "z1-campcenter",
        "say" : [],
        "condition" : "true",
        "do" : ""
      }
    },
  },
  "z1-campcenter" : {
    "name" : "Camp Center",
    "desc.long" : "A makeshift military camp made up of large and small tents placed in a small caldera, with a cooking fire in the center, and the sounds of small conversations flow all around you",
    "desc.short" : "A makeshift camp",
    "container" : {
      "condition" : "true",
      "desc" : "A barrel sits off to the side",
      "say" : [["true", "[@] pries off the cap to look inside"]]
    },
    "dirs" : {
      "north" : {
        "dest" : "z1-boardwalk",
        "say" : [],
        "condition" : "true",
        "do" : ""
      },
      "south" : {
        "dest" : "z1-campstore",
        "say" : [],
        "condition" : "true",
        "do" : ""
      }
    },
  },
  "z1-campstore" : {
    "name" : "Camp Store",
    "desc.long" : "A tent that seems larger than the rest, with shelves filled with food items and weapons, a smell of a old bookstore mixed with canvas fills the air",
    "desc.short" : "A large tent",
    "dirs" : {
      "north" : {
        "dest" : "z1-boardwalk",
        "say" : [],
        "condition" : "true",
        "do" : ""
      },
      "west" : {
        "dest" : "z1-campstorestorage",
        "say" : [["has('standard-key-12')", "[@] used the key to unlock the door"], ["true", "The door appears locked, but the lock is inscribed with the number 12"]],
        "condition" : "has('standard-key-12')",
        "do" : ""
      }
    },
  },
  "z1-campstorestorage" : {
    "name" : "Storage",
    "desc.long" : "A small building built of wood that stands right outside the G{Camp Store}, filled with barrels of mead, cheese, and bread",
    "desc.short" : "A locked storage celler",
    "dirs" : {
      "east" : {
        "dest" : "z1-campstore",
        "say" : [],
        "condition" : "true",
        "do" : ""
      }
    },
  },
}

npcs = {
  "Dockyard Guard" : {
    "z1-docks" : {
      "conditions" : [["quest('z1.main') == -1", "start"], ["true", "secondtime"]],
      "observation" : "A Dockyard Guard watches you",
      "dialouges" : {
        "start" : {
          "dialouge" : [
            ["Dockyard Guard", "Hello [@], it says here on my sheet that you are the new recruit eh?`Well lets hope you fare better than the last one...`Anyway, here is your entry level gear. Oh! And the 'B{General}' wants to speak with you right away, he is in the camp directly 'G{south}' of here."]
          ],
          "do" : "give dagger | stars 10 | quest z1.main 0",
          "options" : [
            ["true", {
              "goto" : "whoareyou",
              "text" : "Who are you?"
            }],
            ["true", {
              "goto" : "lastrecruit",
              "text" : "What happened to the last recruit?"
            }],
            ["true", {
              "goto" : "exit",
              "text" : "Goodbye!"
            }],
          ]
        },
        "secondtime" : {
          "dialouge" : [
            ["Dockyard Guard", "Yes? Do you need something?"]
          ],
          "do" : "",
          "options" : [
            ["true", {
              "goto" : "whoareyou",
              "text" : "Who are you?"
            }],
            ["true", {
              "goto" : "lastrecruit",
              "text" : "What happened to the last recruit?"
            }],
            ["true", {
              "goto" : "exit",
              "text" : "Goodbye!"
            }],
          ]
        },
        "whoareyou" : {
          "dialouge" : [
            ["Dockyard Guard", "I am the Mighty Dockyard Guard! I watch over any and all trading!"]
          ],
          "do" : "",
          "options" : [
            ["true", {
              "goto" : "secondtime",
              "text" : "Nice!"
            }]
          ]
        },
        "lastrecruit" : {
          "dialouge" : [
            ["Dockyard Guard", "Ummm, well he uhhh, you know what? You should just ask the 'B{General}'..."]
          ],
          "do" : "",
          "options" : [
            ["true", {
              "goto" : "secondtime",
              "text" : "Ah, ok."
            }]
          ]
        }
      }
    }
  },
  "Trader Joe" : {
    "z1-bluff-forest" : {
      "conditions" : [["random(10)", "start"]],
      "observation" : "A shady trader watches you from a distance",
      "dialouges" : {
        "start" : {
          "dialouge" : [
            ["Trader Joe", "Good day to you. Care to bargin?"]
          ],
          "do" : "",
          "options" : [
            ["stars > 2", {
              "goto" : "yesfoxnose",
              "text" : "I will take a foxnose"
            }],
            ["stars < 2", {
              "goto" : "nofoxnose",
              "text" : "I will take a foxnose"
            }]
          ]
        },
        "yesfoxnose" : {
          "dialouge" : [
            ["Trader Joe", "Foxnose eh? That will be 2 stars"]
          ],
          "do" : "stars -2 | give foxnose",
          "options" : []
        },
        "nofoxnose" : {
          "dialouge" : [
            ["Trader Joe", "Yeaaaaa, sorry. No stars, no foxnose. Thats how it works around here, now git!"]
          ],
          "do" : "",
          "options" : []
        }
      }
    }
  }
}

quests = {
  "z1.main" : {
    "done" : "You sucessfully found the 'Earth Stone' and moved the bolders",
    "name" : "Campaign",
    "points" : [
      "Head to the main town to receive orders from the General"
    ]
  }
}

items = {
  "dagger" : {
    "type" : "item",
    "name" : "Dagger",
    "desc" : "a short, sharp dagger with a leather grip and a stone as the hilt",
    "value" : 1,
    "craft" : {
      "recipies" : [["stick", "blade"]],
      "locations" : []
    }
  },
  "stick" : {
    "type" : "item",
    "name" : "Stick",
    "desc" : "a very simple wooden stick, still has some leaves attached",
    "value" : 0,
    "craft" : None
  },
  "sand-dollar" : {
    "type" : "item",
    "name" : "Sand Dollar",
    "desc" : "a perfect sand dollar, in near perfect condition",
    "value" : 10,
    "craft" : None
  },
  "standard-key-12" : {
    "type" : "item",
    "name" : "Standard Key #12",
    "desc" : "a old key, inscribed with the number 12",
    "value" : 1,
    "craft" : None
  },
  "healing-brew" : {
    "type" : "potion",
    "name" : "Healing Brew",
    "desc" : "a healing brew made of fish and meat",
    "value" : 3,
    "craft" : {
      "materials" : [["fish"], ["meat"]],
      "locations" : [""]
    }
  },
}

containers = {
  "z1-campcenter" : ["standard-key-12"]
}

maind = {
  "items" : items,
  "npcs" : npcs,
  "world" : world,
  "quests" : quests,
  "containers" : containers
}

htf.encode(json.dumps(maind), KEY, "hurricane/data/assets.dat")