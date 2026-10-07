import pandas as pd
import yt_dlp
from fuzzywuzzy import fuzz

from controls import controls
import time

def getVideoUrl(self, dataframe, index):
  options = {
    "quiet": True,
    "nowarnings": True,
    "noplaylist": True,
    "extract_flat": True
  }
  
  controller = controls()
  
  with yt_dlp.YoutubeDL(options) as ydl:
    print(dataframe)
    songName = dataframe["Song"]
    songArtists = dataframe["Artist"].split(",")

    # Iterate over each song artist
    artistResults = []
    for artist in songArtists:
      audio = None
      while audio is None:
        query = songName + " " + artist

        try:
          results = ydl.extract_info(
            f"ytsearch{controller.searches}:{query}",
            download = False
          )
          audio = results.get("entries", [])
        except Exception as e:
          print(e)

      # Iterate over each audio search result
      for audioInstance in audio:
        resultName = audioInstance.get("title")
        resultArtist = audioInstance.get("uploader")
        resultID = audioInstance.get("id")
      
        # Compare the results
        nameRatio = fuzz.ratio(resultName, songName) * controller.nameWeight
        artistRatio = fuzz.ratio(resultArtist, artist) * controller.artistWeight
        totalRatio = nameRatio + artistRatio

        resultLog = {"ratio": totalRatio, "id": resultID, "name": songName, "artist": resultArtist}
        artistResults.append(resultLog)
    
  if artistResults:
    # Find the highest ratio
    bestMatch = {"ratio": -1}
    for ratio in artistResults:
      if ratio["ratio"] >= bestMatch["ratio"]:
        bestMatch = ratio
    
    bestMatch["confident"] = controller.weightNeeded <= bestMatch["ratio"]
    bestMatch["id"] = "https://www.youtube.com/watch?v=" + bestMatch["id"]
    bestMatch["index"] = index
    bestMatch["CSVArtist"] = dataframe["Artist"]
    bestMatch["albumImageLocation"] = dataframe["Spotify Track Id"]

    self.signals.URL_FOUND.emit(bestMatch)