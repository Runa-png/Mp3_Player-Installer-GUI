from PyQt6.QtCore import (
  Qt,
  QRunnable,
  pyqtSlot,
  pyqtSignal,
  QObject
)

import sqlite3

from config import configs

from math import floor

from ..downloader.downloadURL import downloadURL

class downloadFileWorker(QRunnable):
  class WorkerSignals(QObject):
    STATUS = pyqtSignal(str)
    URL_FOUND = pyqtSignal(dict)
    FINISHED = pyqtSignal()
    UPDATE_PROGRESS = pyqtSignal(int)
  
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.stopEvent = False
    self.signals = self.WorkerSignals()
    self.config = configs()

    self.output = "cache" # Yes im caching the downloads until its finished :)
  
  @pyqtSlot()
  def run(self):
    print(len(self.data))
    length = len(self.data)
    count = 0

    for index in self.data:
      if self.stopEvent:
        return
      
      self.options = {
        "cookiesfrombrowser": ("firefox",),
        "format": "bestaudio/best",
        "outtmpl": f"{self.output}/{self.data[index]["title"]}.%(ext)s",
        "quiet": True,
        "postprocessors": [
          {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
          }
        ],
      }
      
      response = downloadURL(self.data[index]["url"], self.options)

      if response:
        print("UPDATING THE PROGRESS BAR")
        count += 1
        self.signals.UPDATE_PROGRESS.emit(floor((count / length) * 100))
    
    self.signals.FINISHED.emit()