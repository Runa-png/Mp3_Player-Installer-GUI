def filterCommas(songList: list):
  for song in songList:
    song["artist"] = song["artist"].split(",")
  return songList
