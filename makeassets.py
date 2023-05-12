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
do: a list of do strings with conditionals attacked
"""

world = {
  "z1-docks": {
    "name": "Dockyard",
    "desc.long": "You are in a small dockyard with only two ships docked along the pier, there is also faint smell of salty sea air mixed with seaweed that drifts off the ocean",
    "desc.short": "A small dockyard",
    "do": [
      [
        "true",
        "set z1.start 1"
      ]
    ],
    "introtext": [
      [
        "not flag('z1.start')",
        "Welcome to Hurricane! Please sit back and enjoy the adventure."
      ]
    ],
    "dirs": {
      "south": {
        "dest": "z1-boardwalk",
        "say": [
          [
            "not flag('z1.docks.south') and has('dagger')",
            "[@] used Dagger to cut through vines"
          ],
          [
            "not flag('z1.docks.south') and not has('dagger')",
            "There are some spiky vines blocking your way"
          ]
        ],
        "condition": "has('dagger') or flag('z1.docks.south')",
        "do": "set z1.docks.south 1"
      }
    }
  },
  "z1-boardwalk": {
    "name": "Boardwalk",
    "desc.long": "A vary old wooden boardwalk with some chunks missing from it, there are large trees that look for the most part like mangrove trees, and there is the faint sound of seabirds",
    "desc.short": "A old boardwalk",
    "dirs": {
      "north": {
        "dest": "z1-docks",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-eastforest",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-westforest",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-campcenter": {
    "name": "Camp Center",
    "desc.long": "A makeshift military camp made up of large and small tents placed in a small caldera, with a cooking fire in the center, and the sounds of small conversations flow all around you",
    "desc.short": "A makeshift camp",
    "container": {
      "condition": "true",
      "desc": "A barrel sits off to the side",
      "say": [
        [
          "true",
          "You pry off the cap to look inside"
        ]
      ]
    },
    "dirs": {
      "north": {
        "dest": "z1-boardwalk",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-campstore",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-stable",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-campinn",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-stable": {
    "name": "Horse Stable",
    "desc.long": "What looks to be the only permanent structure, a small open building is set up with a few large white and black spotted stallions munching on some hay. The strong scent of horse manure and hay floats around",
    "desc.short": "A small stable",
    "stable": "A large central stable sits nearby",
    "dirs": {
      "west": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-commandtent",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-campstore": {
    "name": "Camp Store",
    "desc.long": "A tent that seems larger than the rest, with shelves filled with food items and weapons, a smell of a old bookstore mixed with canvas fills the air",
    "desc.short": "A large tent",
    "dirs": {
      "north": {
        "dest": "z1-boardwalk",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-campstorestorage",
        "say": [
          [
            "has('standard-key-12')",
            "[@] used the key to unlock the door"
          ],
          [
            "true",
            "The door appears locked, but the lock is inscribed with the number 12"
          ]
        ],
        "condition": "has('standard-key-12')",
        "do": ""
      }
    }
  },
  "z1-campstorestorage": {
    "name": "Storage",
    "desc.long": "A small building built of wood that stands right outside the G{Camp Store}, filled with barrels of mead, cheese, and bread. There is a strong smell of preservatives, dried meat and salt",
    "desc.short": "A locked storage celler",
    "dirs": {
      "east": {
        "dest": "z1-campstore",
        "say": [],
        "condition": "true",
        "do": ""
      }
    },
    "container": {
      "condition": "true",
      "desc": "A old barrel sits in the corner of the room",
      "say": [
        [
          "true",
          "You open the barrel to a smell of fermented ale"
        ]
      ]
    }
  },
  "z1-campinn": {
    "name": "Camp Inn",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-innhallway",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-innhallway": {
    "name": "Inn Hallway",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-campinn",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-innaroom",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-innaroom": {
    "name": "Inna's Room",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-innhallway",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-marieroom",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-marieroom": {
    "name": "Marie's Room",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-innaroom",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-commandtent": {
    "name": "Command Tent",
    "desc.long": "A medium-sized tent with a large wooden table in the center, the table has a very large map with strange figurines perched on. There are banners hanging on all of the tent with different sigals on them",
    "desc.short": "A small tent",
    "dirs": {
      "north": {
        "dest": "z1-stable",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-eastforest": {
    "name": "Forest",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "west": {
        "dest": "z1-boardwalk",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-beach",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-westforest": {
    "name": "Forest",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-boardwalk",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "north": {
        "dest": "z1-rainbluff",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-thechasam",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-rainbluff": {
    "name": "Rain Bluff",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "south": {
        "dest": "z1-westforest",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-thechasam": {
    "name": "The Chasam",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-westforest",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-chasamforest",
        "say": [
          [
            "flag('z1.chasamforest.bridge', '0')",
            "No bridge exists here yet"
          ],
          [
            "flag('z1.chasamforest.bridge', '1')",
            "The bridge is only halfway built"
          ]
        ],
        "condition": "flag('z1.chasamforest.bridge', '2')",
        "do": ""
      }
    }
  },
  "z1-chasamforest": {
    "name": "Forest",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-thechasam",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "north": {
        "dest": "z1-boulderpass",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-darkforest",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-boulderpass": {
    "name": "Bolder Pass",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "south": {
        "dest": "z1-chasamforest",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-darkforest": {
    "name": "Dark Forest",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-chasamforest",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-forestclearing",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-forestclearing": {
    "name": "Forest Clearing",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-darkforest",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-foresthorde",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-foresthorde": {
    "name": "Treasure Horde",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-forestclearing",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-beach": {
    "name": "Beach",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "west": {
        "dest": "z1-eastforest",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "north": {
        "dest": "z1-seacave",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-piratescove",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-cave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-seacave": {
    "name": "Sea Cave",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "south": {
        "dest": "z1-beach",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-piratescove": {
    "name": "Pirates Cove",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "west": {
        "dest": "z1-beach",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "north": {
        "dest": "z1-piratehorde",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-piratehorde": {
    "name": "Treasure Horde",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "south": {
        "dest": "z1-piratescove",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-cave": {
    "name": "Cave",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-beach",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-darkcave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-darkcave": {
    "name": "Dark Cave",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-cave",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-glitteringcave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-glitteringcave": {
    "name": "Glittering Cave",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-darkcave",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-secretcave",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-scarlettcave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-secretcave": {
    "name": "Secret Tunnel",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "east": {
        "dest": "z1-glitteringcave",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-storeceller",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-scarlettcave": {
    "name": "Scarlett's Hiding Place",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "west": {
        "dest": "z1-glitteringcave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-storeceller": {
    "name": "Store Celler",
    "desc.long": "",
    "desc.short": "",
    "dirs": {
      "north": {
        "dest": "z1-campstore",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-secretcave",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  }
}
#############################################################################################
teaserworld = {
  "z1-docks": {
    "name": "Dockyard",
    "desc.long": "You are in a small dockyard with only two ships docked along the pier, there is also faint smell of salty sea air mixed with seaweed that drifts off the ocean",
    "desc.short": "A small dockyard",
    "do": [
      [
        "true",
        "set z1.start 1"
      ]
    ],
    "introtext": [
      [
        "not flag('z1.start')",
        "Welcome to Hurricane! Please sit back and enjoy the adventure."
      ]
    ],
    "dirs": {
      "south": {
        "dest": "z1-boardwalk",
        "say": [
          [
            "not flag('z1.docks.south') and has('dagger')",
            "[@] used Dagger to cut through vines"
          ],
          [
            "not flag('z1.docks.south') and not has('dagger')",
            "There are some spiky vines blocking your way"
          ]
        ],
        "condition": "has('dagger') or flag('z1.docks.south')",
        "do": "set z1.docks.south 1"
      }
    }
  },
  "z1-boardwalk": {
    "name": "Boardwalk",
    "desc.long": "A vary old wooden boardwalk with some chunks missing from it, there are large trees that look for the most part like mangrove trees, and there is the faint sound of seabirds",
    "desc.short": "A old boardwalk",
    "dirs": {
      "north": {
        "dest": "z1-docks",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-campcenter": {
    "name": "Camp Center",
    "desc.long": "A makeshift military camp made up of large and small tents placed in a small caldera, with a cooking fire in the center, and the sounds of small conversations flow all around you",
    "desc.short": "A makeshift camp",
    "container": {
      "condition": "true",
      "desc": "A barrel sits off to the side",
      "say": [
        [
          "true",
          "You pry off the cap to look inside"
        ]
      ]
    },
    "dirs": {
      "north": {
        "dest": "z1-boardwalk",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "south": {
        "dest": "z1-campstore",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "east": {
        "dest": "z1-stable",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-campinn",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-stable": {
    "name": "Horse Stable",
    "desc.long": "What looks to be the only permanent structure, a small open building is set up with a few large white and black spotted stallions munching on some hay. The strong scent of horse manure and hay floats around",
    "desc.short": "A small stable",
    "stable": "A large central stable sits nearby",
    "dirs": {
      "west": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  },
  "z1-campstore": {
    "name": "Camp Store",
    "desc.long": "A tent that seems larger than the rest, with shelves filled with food items and weapons, a smell of a old bookstore mixed with canvas fills the air",
    "desc.short": "A large tent",
    "dirs": {
      "north": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-campstorestorage",
        "say": [
          [
            "has('standard-key-12')",
            "[@] used the key to unlock the door"
          ],
          [
            "true",
            "The door appears locked, but the lock is inscribed with the number 12"
          ]
        ],
        "condition": "has('standard-key-12')",
        "do": ""
      }
    },
    "store": {
      "multiplier": 1,
      "desc": "A dusty store counter sits along the far wall",
      "condition": "quest('z1.campstore.unlock') == 1",
      "items": [
        [
          "true",
          "sweet-apple"
        ],
        [
          "true",
          "raw-potato"
        ]
      ]
    }
  },
  "z1-campstorestorage": {
    "name": "Storage",
    "desc.long": "A small building built of wood that stands right outside the G{Camp Store}, filled with barrels of mead, cheese, and bread. There is a strong smell of preservatives, dried meat and salt",
    "desc.short": "A locked storage celler",
    "dirs": {
      "east": {
        "dest": "z1-campstore",
        "say": [],
        "condition": "true",
        "do": ""
      }
    },
    "container": {
      "condition": "true",
      "desc": "A old barrel sits in the corner of the room",
      "say": [
        [
          "true",
          "You open the barrel to a smell of fermented ale"
        ]
      ]
    }
  },
  "z1-campinn": {
    "name": "Camp Inn",
    "desc.long": "The largest tent around, so big that it seems to have a hallway and rooms behind the counter. There is hustle and bustle all around as people move about their daily activities",
    "desc.short": "A very large tent",
    "dirs": {
      "east": {
        "dest": "z1-campcenter",
        "say": [],
        "condition": "true",
        "do": ""
      },
      "west": {
        "dest": "z1-innhallway",
        "say": [
          [
            "true",
            "The door seems to be locked"
          ]
        ],
        "condition": "false",
        "do": ""
      }
    }
  },
  "z1-innhallway": {
    "name": "Inn Hallway",
    "desc.long": "",
    "desc.short": "A small hallway",
    "dirs": {
      "east": {
        "dest": "z1-campinn",
        "say": [],
        "condition": "true",
        "do": ""
      }
    }
  }
}

npcs = {
  "Dockyard Guard": {
    "z1-docks": {
      "conditions": [
        [
          "quest('z1.main') == -1",
          "start"
        ],
        [
          "true",
          "secondtime"
        ]
      ],
      "observation": [
        [
          "true",
          "A Dockyard Guard watches you"
        ]
      ],
      "dialouges": {
        "start": {
          "dialouge": [
            [
              "Dockyard Guard",
              "Hello [@], it says here on my sheet that you are the new recruit eh?`Well lets hope you fare better than the last one...`Anyway, here is your entry level gear, and the 'B{General}' wants to speak with you right away, he is in the camp directly 'Y{south}' of here."
            ]
          ],
          "do": "give dagger | stars 10 | quest z1.main 0",
          "options": [
            [
              "true",
              {
                "goto": "whoareyou",
                "text": "Who are you?"
              }
            ],
            [
              "true",
              {
                "goto": "lastrecruit",
                "text": "What happened to the last recruit?"
              }
            ],
            [
              "true",
              {
                "goto": "exit",
                "text": "Goodbye!"
              }
            ]
          ]
        },
        "secondtime": {
          "dialouge": [
            [
              "Dockyard Guard",
              "Yes? Do you need something?"
            ]
          ],
          "do": "",
          "options": [
            [
              "true",
              {
                "goto": "whoareyou",
                "text": "Who are you?"
              }
            ],
            [
              "true",
              {
                "goto": "lastrecruit",
                "text": "What happened to the last recruit?"
              }
            ],
            [
              "true",
              {
                "goto": "exit",
                "text": "Goodbye!"
              }
            ]
          ]
        },
        "whoareyou": {
          "dialouge": [
            [
              "Dockyard Guard",
              "I am the Mighty Dockyard Guard! I watch over any and all trading!"
            ]
          ],
          "do": "",
          "options": [
            [
              "true",
              {
                "goto": "secondtime",
                "text": "Nice!"
              }
            ]
          ]
        },
        "lastrecruit": {
          "dialouge": [
            [
              "Dockyard Guard",
              "Ummm, well he uhhh, you know what? You should just ask the 'B{General}'..."
            ]
          ],
          "do": "",
          "options": [
            [
              "true",
              {
                "goto": "secondtime",
                "text": "Ah, ok."
              }
            ]
          ]
        }
      }
    }
  },
  "Inn Keeper": {
    "z1-campinn": {
      "conditions": [
        [
          "quest('z1.innkeeper.stew') == -1",
          "start"
        ],
        [
          "quest('z1.innkeeper.stew') in [0, 1]",
          "waiting"
        ],
        [
          "quest('z1.innkeeper.stew') == 2",
          "done"
        ]
      ],
      "observation": [
        [
          "true",
          "The inn keeper is stirring a massive pot of soup in the corner"
        ]
      ],
      "dialouges": {
        "start": {
          "dialouge": [
            [
              "Innkeeper",
              "Well hello there young one! What brings you to the inn?"
            ],
            [
              "You",
              "Not much, just looking around. Who are you?"
            ],
            [
              "Innkeeper",
              "Well I am Frank of course I am!"
            ],
            [
              "You",
              "I see! Hello Frank, what are you doing over there?"
            ],
            [
              "Frank",
              "Well you see, I am trying to make soup for my husband Fred, but it just does not taste right of course!"
            ],
            [
              "You",
              "Hmmm, do you need any help?"
            ],
            [
              "Frank",
              "Well, yes I would of course! Lets see...`If you could grab me a B{Foxnose} plant that would be terrific. There is sometimes a G{Shady Trader} that comes to visit the Y{Town Square} that carries them of course. You will need some stars to get some from him, I would think B{15 stars} should be enough."
            ]
          ],
          "do": "stars 15 | quest z1.innkeeper.stew 0",
          "options": [
            [
              "true",
              {
                "goto": "exit",
                "text": "No problem, be right back!"
              }
            ]
          ]
        },
        "hurry": {
          "dialouge": [
            [
              "Frank",
              "Please hurry of course!"
            ]
          ],
          "do": "exit",
          "options": []
        },
        "done": {
          "dialouge": [
            [
              "Frank",
              "Thank you so much for helping out with that soup, it really means a lot to me."
            ]
          ],
          "do": "exit",
          "options": [
            [
              "true",
              {
                "goto": "exit",
                "text": "No problem!"
              }
            ]
          ]
        },
        "waiting": {
          "dialouge": [
            [
              "Frank",
              "Did you find any yet?"
            ]
          ],
          "do": "",
          "options": [
            [
              "quest('z1.innkeeper.stew') == 0 and has('foxnose')",
              {
                "goto": "hasfoxnose",
                "text": "Here is your Foxnose"
              }
            ],
            [
              "quest('z1.innkeeper.stew') == 1 and has('goat-meat')",
              {
                "goto": "hasgoatmeat",
                "text": "Here is your Goat Meat *ew*"
              }
            ],
            [
              "quest('z1.innkeeper.stew') == 0 and not has('foxnose')",
              {
                "goto": "hurry",
                "text": "Not yet"
              }
            ],
            [
              "quest('z1.innkeeper.stew') == 1 and not has('goat-meat')",
              {
                "goto": "hurry",
                "text": "Not yet"
              }
            ]
          ]
        },
        "hasfoxnose": {
          "dialouge": [
            [
              "Frank",
              "Thank you so much young one!`I must say you are a rather helpful helper. Would you do one more favor for me?"
            ],
            [
              "You",
              "Sure! What do you need?"
            ],
            [
              "Frank",
              "My stew is a bit bland right now, do you think you could find some G{Goat Meat} to help spice it up? It used to be sold in the Y{Camp Store}, but I am afraid they do not sell it anymore, though there were rumors..."
            ],
            [
              "You",
              "Rumors?`Of what?"
            ],
            [
              "Frank",
              "Well...`At least I heard...`There may still be some locked in the store's storage. If you can find your way in you might be able to grab some B{Goat Meat} without anyone knowing."
            ]
          ],
          "do": "quest z1.innkeeper.stew 1",
          "options": [
            [
              "true",
              {
                "goto": "exit",
                "text": "Alright, I will get the meat!"
              }
            ]
          ]
        },
        "hasgoatmeat": {
          "dialouge": [
            [
              "Frank",
              "You found some! My that is wonderful of course! This is the perfect thing for my soup!"
            ],
            [
              "You",
              "Sure! Glad I could help!"
            ],
            [
              "Frank",
              "Now if you wait just a moment...`A little longer...`...`...`YES!`My stew is finaly done! Time to tell Fred.`OH FRE-ED!"
            ],
            [
              "Fred",
              "Huh? Did you call me Frank?"
            ],
            [
              "Frank",
              "Yes! This young travler helped me make my famous stew!"
            ],
            [
              "Fred",
              "My, that is good stew, thank you...`I am so very sorry, but what was your name?"
            ],
            [
              "You",
              "My name is [@], I am the new recruit here."
            ],
            [
              "Fred",
              "I see! Well, thank you for helping my husband with his stew.`Between you and me, he is not the best cook."
            ],
            [
              "Frank",
              "Hey!"
            ],
            [
              "Fred",
              "Kidding, kidding. Well, have a good day [@]!"
            ]
          ],
          "do": "quest z1.innkeeper.stew 2",
          "options": [
            [
              "true",
              {
                "goto": "exit",
                "text": "You too!"
              }
            ]
          ]
        }
      }
    }
  },
  "Shady Trader": {
    "z1-campcenter": {
      "conditions": [
        [
          "random(3) and not flag('z1.npc.shady-trader.first')",
          "first"
        ],
        [
          "random(3) and flag('z1.npc.shady-trader.first')",
          "start"
        ]
      ],
      "observation": [
        [
          "true",
          "A shady trader watches you from a distance"
        ]
      ],
      "dialouges": {
        "first": {
          "dialouge": [
            [
              "Shady Trader",
              "Yea? Who are you and what do you want?"
            ],
            [
              "You",
              "My name is [@], who are you?"
            ],
            [
              "Shady Trader",
              "[@] huh? Interesting name.`All you need to know is that I am a trader of wares. Some legal... some not, all of which cost G{stars}."
            ]
          ],
          "do": "set z1.npc.shady-trader.first 1",
          "options": [
            [
              "true",
              {
                "goto": "start",
                "text": "Alright then"
              }
            ]
          ]
        },
        "start": {
          "dialouge": [
            [
              "Shady Trader",
              "Care to bargin?"
            ]
          ],
          "do": "",
          "options": [
            [
              "stars >= 10",
              {
                "goto": "yesfoxnose",
                "text": "I will take a foxnose"
              }
            ],
            [
              "stars < 10",
              {
                "goto": "nofoxnose",
                "text": "I will take a foxnose"
              }
            ],
            [
              "quest('z1.campstore.unlock') == 0",
              {
                "goto": "storehandle",
                "text": "Do you know anything about a store handle?"
              }
            ],
            [
              "true",
              {
                "goto": "exit",
                "text": "No thanks"
              }
            ]
          ]
        },
        "yesfoxnose": {
          "dialouge": [
            [
              "Trader Joe",
              "Foxnose eh? That will be 10 stars"
            ]
          ],
          "do": "stars -10 | give foxnose",
          "options": [
            [
              "true",
              {
                "goto": "pleasure",
                "text": "Deal"
              }
            ]
          ]
        },
        "nofoxnose": {
          "dialouge": [
            [
              "Trader Joe",
              "Yeaaaaa, sorry. G{Foxnose} is a crisp 10 stars. No stars, no G{foxnose}. Thats how it works around here kid."
            ]
          ],
          "do": "exit",
          "options": []
        },
        "pleasure": {
          "dialouge": [
            [
              "Trader Joe",
              "Pleasure doing business with you."
            ]
          ],
          "do": "exit",
          "options": []
        },
        "storehandle": {
          "dialouge": [
            [
              "Trader",
              "A... what?"
            ],
            [
              "You",
              "A handle. One made for a store cupboard?"
            ],
            [
              "Trader",
              "Hmph, fine. I may have it.`A nice 20 stars would make sure I tell you the right information..."
            ]
          ],
          "do": "",
          "options": [
            [
              "stars >= 20",
              {
                "goto": "yesstorehandle",
                "text": "Here is 20 stars"
              }
            ],
            [
              "stars < 20",
              {
                "goto": "nostorehandle",
                "text": "I do not have 20 stars"
              }
            ]
          ]
        },
        "yesstorehandle": {
          "dialouge": [
            [
              "Trader",
              "Why thank you! Here is your G{store handle}."
            ],
            [
              "You",
              "Stealing is not cool, I could report you to the B{General} you know."
            ],
            [
              "Trader",
              "I have no idea what you are talking about, I found that piece of shiny metal just laying about."
            ]
          ],
          "do": "stars -20 | give store-cabinet-handle",
          "options": [
            [
              "true",
              {
                "goto": "pleasure",
                "text": "Thanks anyway"
              }
            ]
          ]
        },
        "nostorehandle": {
          "dialouge": [
            [
              "Trader",
              "Come back later, I do not work for free."
            ]
          ],
          "do": "exit",
          "options": []
        }
      }
    }
  },
  "Shop Owner": {
    "z1-campstore": {
      "conditions": [
        [
          "quest('z1.campstore.unlock') == -1",
          "start"
        ],
        [
          "quest('z1.campstore.unlock') == 0",
          "waiting"
        ],
        [
          "quest('z1.campstore.unlock') == 1",
          "done"
        ]
      ],
      "observation": [
        [
          "quest('z1.campstore.unlock') != 1",
          "The store owner sits in a chair behind the counter, looking rather board"
        ],
        [
          "true",
          "The store owner is standing behind the counter"
        ]
      ],
      "dialouges": {
        "start": {
          "dialouge": [
            [
              "You",
              "Hi! What do you have for sale?"
            ],
            [
              "Shop Owner",
              "Huh? Oh. Nothing. At least, nothing NOW. We used to have food and supplies but someone stole the handle from the closet over there."
            ]
          ],
          "do": "",
          "options": [
            [
              "true",
              {
                "goto": "stealhandlequestion",
                "text": "Stole the... handle?"
              }
            ],
            [
              "true",
              {
                "goto": "gethandleplea",
                "text": "Do you need help getting it back?"
              }
            ]
          ]
        },
        "stealhandlequestion": {
          "dialouge": [
            [
              "Shop Owner",
              "Yes.`Someone actually stole the handle off my cabinet.`Now what am I supposed to do?"
            ]
          ],
          "do": "",
          "options": [
            [
              "true",
              {
                "goto": "gethandleplea",
                "text": "I have no idea, I might be able to help find it?"
              }
            ]
          ]
        },
        "gethandleplea": {
          "dialouge": [
            [
              "Shop Owner",
              "Would you do that, thank you so much! That would help out so much.`It has become a pigsty in here of late. When people cannot get their daily food they can get pretty mad."
            ]
          ],
          "do": "quest z1.campstore.unlock 0",
          "options": [
            [
              "true",
              {
                "goto": "thankyouaccept",
                "text": "Your welcome!"
              }
            ]
          ]
        },
        "waiting": {
          "dialouge": [
            [
              "Jodie",
              "Do you have my handle yet?"
            ]
          ],
          "do": "",
          "options": [
            [
              "has('store-cabinet-handle')",
              {
                "goto": "hashandle",
                "text": "Yes I do!"
              }
            ],
            [
              "not has('store-cabinet-handle')",
              {
                "goto": "nohashandle",
                "text": "No I do not"
              }
            ]
          ]
        },
        "hashandle": {
          "dialouge": [
            [
              "Jodie",
              "Are you sure? Let me see if it fits.`...`...`It does! By the rocks you are a lifesaver! Have a few stars as gratitude."
            ],
            [
              "You",
              "You are very welcome. Thank you for the stars!"
            ],
            [
              "Jodie",
              "Just so you know the store is open now too so if you every need supplies, I got 'em!"
            ]
          ],
          "do": "quest z1.campstore.unlock 1",
          "options": [
            [
              "true",
              {
                "goto": "exit",
                "text": "I will keep that in mind"
              }
            ]
          ]
        },
        "thankyouaccept": {
          "dialouge": [
            [
              "Shop Owner",
              "Again, thank you so much! I really appreatiate it."
            ],
            [
              "You",
              "I'll be back with your handle, do you have any idea who may have taken it?"
            ],
            [
              "Shop Owner",
              "No, but whoever it was has to be pretty B{shady}."
            ],
            [
              "You",
              "Alright, well then I will be back... I never caught your name?"
            ],
            [
              "Store Owner",
              "Jodie. At least that is what most call me."
            ],
            [
              "You",
              "Nice to meet you Jodie, I will be right back your handle."
            ],
            [
              "Jodie",
              "Thanks [@]!"
            ],
            [
              "You",
              "How do you know my name?"
            ],
            [
              "Jodie",
              "Word travels fast here. It was nice meeting you [@], and thanks again for bringing back my handle!"
            ]
          ],
          "do": "exit",
          "options": []
        },
        "nohashandle": {
          "dialouge": [
            [
              "Jodie",
              "Alright, take your time."
            ]
          ],
          "do": "exit",
          "options": []
        }
      }
    }
  }
}

quests = {
  "z1.main" : {
    "done" : "You sucessfully found the 'G{Earth Stone}' and moved the bolders",
    "name" : "Campaign",
    "points" : [
      "Head to the main town to receive orders from the B{General}",
      "Yeet a child off a cliff"
    ]
  },
  "z1.innkeeper.stew" : {
    "done" : "You sucessfully found all the ingredients and gave them to B{Frank} to make a soup",
    "name" : "Studious Stew",
    "points" : [
      "Find a 'G{Foxnose}' plant, Frank said that a shifty travler sometimes carries them",
      "Find a slab of 'G{Goat Meat}', usually stored in meat drying racks"
    ]
  },
  "z1.campstore.unlock" : {
    "done" : "You sucessfully found the Store Handle and returned it to B{Jodie}",
    "name" : "Missing Handle",
    "points" : [
      "Find the G{Store Handle} and give it back to B{Jodie}"
    ]
  }
}

items = {
  "dagger" : {
    "name" : "Dagger",
    "desc" : "a short, sharp dagger with a leather grip and a stone as the hilt",
    "value" : 20,
    "craft" : {
      "recipies" : [{
        "items" : ["stick", "blade"],
        "locations" : []
      }],
    }
  },
  "stick" : {
    "name" : "Stick",
    "desc" : "a very simple wooden stick, still has some leaves attached",
    "value" : 5,
    "craft" : None
  },
  "sand-dollar" : {
    "name" : "Sand Dollar",
    "desc" : "a perfect sand dollar, in near perfect condition",
    "value" : 100,
    "craft" : None
  },
  "foxnose" : {
    "name" : "Foxnose",
    "desc" : "a short shrub, has orange and yellow flowers",
    "value" : 10,
    "craft" : None
  },
  "goat-meat" : {
    "name" : "Goat Meat",
    "desc" : "a slab of cured meat, smells of salt",
    "value" : 20,
    "craft" : None
  },
  "standard-key-12" : {
    "name" : "Standard Key #12",
    "desc" : "a old key, inscribed with the number 12",
    "value" : 10,
    "craft" : None
  },
  "store-cabinet-handle" : {
    "name" : "Store Cabinet Handle",
    "desc" : "a old-style cabinet handle for the Camp Store",
    "value" : 10,
    "craft" : None
  },
  "healing-brew" : {
    "name" : "Healing Brew",
    "desc" : "a healing brew made of fish and meat",
    "value" : 30,
    "craft" : None
  },
  "sweet-apple" : {
    "name" : "Sweet Apple",
    "desc" : "a apple with a sweet gooey coating",
    "value" : 10,
    "craft" : None
  },
  "raw-potato" : {
    "name" : "Raw Potato",
    "desc" : "a regular, slightly hard raw potato",
    "value" : 10,
    "craft" : None
  },
}

containers = {
  "z1-campcenter" : ["standard-key-12"],
  "z1-campstorestorage" : ["goat-meat"],
}

maind = {
  "items" : items,
  "npcs" : npcs,
  #"world" : world,
  "world": teaserworld,
  "quests" : quests,
  "containers" : containers
}

print("Starting Encode...")
htf.encode(json.dumps(maind), KEY, "hurricane/data/assets.dat")
print("Done")