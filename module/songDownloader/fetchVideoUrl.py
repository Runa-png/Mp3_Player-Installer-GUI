import yt_dlp
from fuzzywuzzy import fuzz, process
import math

def fetchVideoUrl(dictList: list, controller: dict):
  options = {
    "quiet": True,
    "nowarnings": True
  }

  with yt_dlp.YoutubeDL(options) as ydl:
    # DELETE [{'name': 'World is mine', 'artist': ['yuigot', 'Yachiyo Runami(cv.Saori Hayami)', 'Cosmic Princess Kaguya!']}]
    
    # Iterating over each artist is important for some studios who claimed their music
    totalSongList = []
    for song in dictList:
      videoData = []
      for artist in song["artist"]:
        results = ydl.extract_info(
          f"ytsearch3:{song["name"]} {artist}",
          download = False
        )

        video = results.get("entries", [])
        if not video:
          continue

        # Get Video Details
        
        for i in video:
          title = i.get("title")
          uploader = i.get("uploader")
          id = i.get("id")
          
          nameWeight = fuzz.ratio(title, song["name"]) * controller.nameWeight
          artistWeight = fuzz.ratio(uploader, artist) * controller.artistWeight
          totalWeight = nameWeight + artistWeight

          videoData.append({"name": song["name"], "url": id, "uploader": uploader, "ratio": math.floor(totalWeight)})
      
      bestMatch = {"ratio": -1} # Not risking it with 0
      for authorRecommendation in videoData:
        if authorRecommendation["ratio"] > bestMatch["ratio"]:
          bestMatch = authorRecommendation
      if bestMatch["ratio"] <= controller.weightNeeded:
        bestMatch["confident"] = False
      else:
        bestMatch["confident"] = True
      
      totalSongList.append(bestMatch)
    return (totalSongList)
