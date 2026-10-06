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

import shutil
import os

class downloadFileWorker(QRunnable):
  class WorkerSignals(QObject):
    STATUS = pyqtSignal(str)
    FINISHED = pyqtSignal()
    UPDATE_PROGRESS = pyqtSignal(list)
    FAILED_DOWNLOAD = pyqtSignal(int)
  
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

    connection = database = sqlite3.connect("database.db")
    cursor = connection.cursor()
    
    cachedData = []
    for index in self.data:
      print(self.data[index])
      
      # Stop when the mainWindow is closed
      if self.stopEvent:
        return
      
      # Don't download if the song has already been downloaded
      exists = cursor.execute("SELECT * FROM songs WHERE name = ? AND artist = ?", (self.data[index]["title"], self.data[index]["artist"])).fetchone()
      
      self.options = {
        "cookiesfrombrowser": ("firefox",),
        "format": "bestaudio/best",
        "outtmpl": f'{self.output}/{self.data[index]["title"]}.%(ext)s',
        "quiet": True,
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
      }
      
      if not exists:
        response = downloadURL(self.data[index]["url"], self.options)

        if response["successful"]:
          # Store the name and artist for adding to the database
          newCacheStatus = {"name": self.data[index]["title"], "artist": self.data[index]["artist"], "filename": self.data[index]["title"] + ".mp3"}
          cachedData.append(newCacheStatus)
        else:
          print("Failed to download")
          self.signals.FAILED_DOWNLOAD.emit(index)
      
      # Update the progress bar
      count += 1
      self.signals.UPDATE_PROGRESS.emit([floor((count / length) * 100), index])
    
    if cachedData:
      print(cachedData)

      os.makedirs(self.config.CreatePlaylist.musicLocation, exist_ok=True)

      # Now we push the cache into the actual music folder
      for cached in cachedData:
        fileLocation = "cache/" + cached["filename"]
        fileDestination = self.config.CreatePlaylist.musicLocation + "/" + cached["filename"]

        shutil.copy2(fileLocation, fileDestination)
        cursor.execute("INSERT INTO songs (name, artist, location) VALUES (?,?,?)", (cached["name"], cached["artist"], fileDestination))

      connection.commit()
      connection.close()

      shutil.rmtree("cache", ignore_errors=True)

    self.signals.FINISHED.emit()