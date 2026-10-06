import yt_dlp

def downloadURL(url, options):
  passed = False
  print(url)
  while not passed:
    try:
      with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)
        passed = True
    except Exception as e:
      if "is not a valid URL" in str(e) or "Video unavailable" in str(e):
        return False
  return True