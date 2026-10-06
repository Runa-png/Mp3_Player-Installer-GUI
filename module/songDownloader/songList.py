def songList(csvFile):
  filteredCsv = (csvFile[["Song", "Artist"]])
  
  # Create a list of dictionaries with name and artist
  songList = []
  for songIndex in range(0, len(filteredCsv)):
    songDataframe = filteredCsv.iloc[songIndex-1]
    newDict = {"name": songDataframe["Song"], "artist": songDataframe["Artist"]}
    songList.append(newDict)
  
  return songList