from mutagen import File

def extractAlbumArt(self, location):
  audio = File(location)
  artwork = None

  if not audio or not audio.tags:
    return artwork

  if "APIC:" in audio.tags:
    artwork = audio.tags["APIC:"].data
  else:
    for tag in audio.tags.values():
      if hasattr(tag, "data") and hasattr(tag, "mime"):
        artwork = tag.data
        break
  return artwork