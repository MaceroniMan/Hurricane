# Hide That File is a simple program to encode text with a key
import hashlib, math

def __circleadd(num, addend, circlepoint):
  for onnum in range(addend%255):
    if num >= circlepoint:
      num = 0
    num += 1
  return num

def __circlesub(num, addend, circlepoint):
  for onnum in range(addend%255):
    num -= 1
    if num <= 0:
      num = circlepoint
  return num

def __pswd(word):
  numbers = ""
  for char in word:
    numbers += str(ord(char))
  return int(numbers)

def encode(text, key):
  if type(key) == int:
    pass
  elif type(key) == str:
    key = __pswd(key)
  else:
    raise TypeError("invalid key type, must be string or int")

  hash = hashlib.sha512(str(text+str(key)).encode()).hexdigest()
  pswdhash = hashlib.sha512(str(key).encode()).hexdigest()
  stringlength = len(text)
  placeevery = math.ceil(stringlength / 128)
  placecounter = 0
  counter = 0
  newnums = []
  textcounter = 0
  totaltextcounter = round(__pswd(pswdhash[0]))
  for char in text:
    if textcounter == totaltextcounter:
      textcounter = 0

    if counter == placeevery:
      newnums.append(__circleadd(ord(hash[placecounter]), key + textcounter, 255))
      placecounter += 1
      counter = 0
      textcounter += 1

    if textcounter == totaltextcounter:
      textcounter = 0

    newnums.append(__circleadd(ord(char), key + textcounter, 255))
    counter += 1
    textcounter += 1

  left = 128 - placecounter
  for item in range(left):
    if textcounter == totaltextcounter:
      textcounter = 0
    newnums.append(__circleadd(ord(hash[item+placecounter]), key + textcounter, 255))
    textcounter += 1

  return bytes(newnums)

def decode(bin_data, key):
  if type(key) == int:
    pass
  elif type(key) == str:
    key = __pswd(key)
  else:
    raise TypeError("invalid key type, must be string or int")

  pswdhash = hashlib.sha512(str(key).encode()).hexdigest()
  stringlength = len(bin_data) - 128

  if stringlength % 128 != 0:
    chars = math.floor((stringlength) / 128) + 1
  else:
    chars = math.floor((stringlength) / 128)

  if chars == 0:
    chars = 1
  counter = 0
  charcounter = 0
  leftoff = 0
  newchars = []
  for char in bin_data:
    leftoff += 1
    if charcounter == stringlength:
      break

    if counter == chars:
      counter = 0
      newchars.append([1, char])
    else:
      newchars.append([0, char])
      charcounter += 1
      counter += 1

  for char2 in bin_data[leftoff-1:]:
    newchars.append([1, char2])

  unenc = []
  newhash = ""
  totaltextcounter = round(__pswd(pswdhash[0]))
  textcounter = 0
  for newchar in newchars:
    if textcounter == totaltextcounter:
      textcounter = 0
    if newchar[0] == 0:
      unenc.append(chr(__circlesub(newchar[1], key + textcounter, 255)))
    else:
      newhash += chr(__circlesub(newchar[1], key + textcounter, 255))
    textcounter += 1

  realtext = ''.join(unenc)

  if not hashlib.sha512(str(realtext+str(key)).encode()).hexdigest() == newhash:
    return None
  else:
    return realtext
