import yt_dlp

def downloadSongs(urlDict: dict, controller: dict):
  passed = False
  while not passed:
    output = controller.musicOutput
    name = urlDict["name"]
    url = urlDict["url"]
    
    options = {
      "format": "bestaudio/best",
      "outtmpl": f"{output}/{name}.%(ext)s",
      "quiet": True,
      "postprocessors": [
        {
          "key": "FFmpegExtractAudio",
          "preferredcodec": "mp3",
          "preferredquality": "192",
        }
      ],
    }

    try:
      with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)
        passed = True
    except Exception as e:
      print(e)
      pass

  return {"location": f"{output}/{name}.mp3", "name": name}