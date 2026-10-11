from fuzzywuzzy import fuzz

def calculateAccuracy(data, comparison, dictKey):
  convertDict = {
    "Title": "songName",
    "Artist": "artistName",
    "Album": "albumName"
  }
  
  actualDictionaryKey = convertDict[dictKey]

  dictionaryEntry = (data[actualDictionaryKey].lower())
  print(dictionaryEntry)

  data["accuracy"] = fuzz.partial_ratio((comparison).lower(), dictionaryEntry)

  return (data)
