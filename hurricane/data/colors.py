import os

try:
  import colorama
except:
  pass

# returns a list of printable colors
def getcolors():

  raise SyntaxError("old_colors_method_called")
  colors = {
    "red" : "",
    "yellow" : "",
    "green" : "",
    "bold" : "",
    "blue" : "",
    "reset" : "",
    "background" : "",
    "underline" : "",
    "supported" : False
  }
  
  if os.name == "nt":
    try:
      colors["reset"] = colorama.Style.RESET_ALL
      colors["bold"] = colorama.Style.BRIGHT
      colors["green"] = colorama.Fore.GREEN
      colors["yellow"] = colorama.Fore.YELLOW
      colors["blue"] = colorama.Fore.CYAN
      colors["red"] = colorama.Fore.RED
      colors["background"] = colorama.Back.WHITE
      colors["underline"] = colorama.Style.UNDERLINE
      colors["supported"] = True
    except:
      pass
  else:
    colors["reset"] = "\033[0m"
    colors["bold"] = "\033[01m"
    colors["green"] = "\033[32m"
    colors["yellow"] = "\033[93m"
    colors["blue"] = "\033[96m"
    colors["red"] = "\033[31m"
    colors["background"] = "\033[0;30;47m"
    colors["underline"] = "\033[4m"
    colors["supported"] = True

  return colors