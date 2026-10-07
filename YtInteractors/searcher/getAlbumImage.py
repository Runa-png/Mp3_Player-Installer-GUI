from PyQt6.QtGui import (QPixmap, QIcon)
from mutagen.mp3 import MP3
from mutagen.id3 import APIC

def getAlbumImage(mp3Location):
  audioImage = MP3(mp3Location)
  for tag in audioImage.tags.values():
    if isinstance(tag, APIC):
      pixmap = QPixmap()
      pixmap.loadFromData(tag.data)

      return QIcon(pixmap)
  return QIcon()