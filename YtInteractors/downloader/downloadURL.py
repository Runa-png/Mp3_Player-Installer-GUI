import yt_dlp

def downloadURL(url, options):
  # These are error messages that will break the loop
  error_messages = (
    "is not a valid URL",
    "Video unavailable",
    "You've asked yt-dlp to download the URL",
    "Unable to download webpage: HTTPSConnection",
    "This video is unavailable",
    "Incomplete YouTube ID",
    "HTTP Error 404"
  )
  
  passed = False
  while not passed:
    try:
      with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download(url)
        passed = True
    except Exception as e:
      # Im really sorry
      if any(message in str(e) for message in error_messages):
        return {"successful": False}
  return {"successful": True}