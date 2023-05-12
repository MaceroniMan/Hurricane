# Pretty printing XML after parsing
# it from dictionary
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
import hurricane.data.htf as htf, json
import xml.etree.ElementTree as E

def parsel(root):
  out = []
  for child in root:
    out.append(parsee(child))

  return out

def parsee(child):
  ctype = child.attrib["type"]
  if ctype == "str":
    return str(child.text)
  if ctype == "int":
    return int(child.text)
  if ctype == "dict":
    return parsed(child)
  if ctype == "list":
    return parsel(child)
    
def parsed(root):
  out = {}
  for child in root:
    out[child.tag] = parsee(child)

  return out

def get():
  rdata = None
  while rdata == None:
    fname = "" + input("name of savegame? ")
    password = input("password of savegame? ")

    try:
      rdata = json.loads(htf.decode("hurricane/saves/" + fname, password))
    except TypeError:
      print("incorrect username/password (enter to continue)")
      input()

  return rdata, password, fname

print(" Hurricane Savegame Editor")
print("===========================")
data, passwd, fname = get()

xml = dicttoxml(data)
dom = parseString(xml)
 
with open("edit.xml", "w") as file:
  file.write(dom.toprettyxml())

input("savegame exported to 'exit.xml', press enter to save changes")

tree = E.parse('edit.xml')
root = tree.getroot()

s = parsed(root)

htf.encode(json.dumps(s), passwd, "hurricane/saves/" + fname)