from PyQt6.QtWidgets import (
  QPushButton,
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QScrollArea
)

from PyQt6.QtCore import (
  Qt,
  QSize
)

from PyQt6.QtGui import (
  QIcon
)

from config import configs
import os
import sqlite3

class CreatePlaylistWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.setContentsMargins(0,0,0,0)
    self.config = configs()

    topLayout = QVBoxLayout(self)
    titleLabel = QLabel("Create Playlist")
    titleLabel.setStyleSheet("color: white; font-size: 25px; font-weight: 900; text-decoration: underline")

    scrollableArea = QScrollArea()
    scrollableArea.setWidgetResizable(True)
    
    scrollableAreaContainerWidget = QWidget()
    self.scrollableAreaContainer = QVBoxLayout(scrollableAreaContainerWidget)

    scrollableArea.setWidget(scrollableAreaContainerWidget)

    scrollableAreaContainerWidget.setStyleSheet("background-color: rgb(100,0,0)")
    
    topLayout.addWidget(titleLabel, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    topLayout.addWidget(scrollableArea, stretch=1)

    # Just run the search function
    self.readMusic()
  
  def readMusic(self):
    searchFolder = self.config.CreatePlaylist.musicLocation
    folder = os.listdir(searchFolder)

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    songDataList = []
    # Iterate over each file in the folder
    for file in folder:
      location = f"{searchFolder}/{file}"
      
      filename, fileExtension = os.path.splitext(location)
      # Nice try slipping in a txt file or something
      if fileExtension != ".mp3":
        continue

      data = cursor.execute("SELECT * FROM songs WHERE location = ?", (location,)).fetchone()

      title = data[0]
      artist = data[1]
      
      newDataDict = {"title": title, "artist": artist, "location": location}
      songDataList.append(newDataDict)
    
    self.widgetList = {}

    length = len(songDataList)
    count = 0
    # Iterate over each song in the list
    for songDict in songDataList:
      containerWidget = QWidget()
      containerLayout = QHBoxLayout(containerWidget)

      # Widgets to be in the layout
      nameLabel = QLabel(songDict["title"][:20])
      artistLabel = QLabel(songDict["artist"][:20])

      playlistButton = QPushButton("Add")

      # Add to the layout
      containerLayout.addWidget(nameLabel)
      containerLayout.addWidget(artistLabel)
      containerLayout.addWidget(playlistButton)

      # Add widgets to the indexed dict
      self.widgetList[count] = {"name": nameLabel, "artist": artistLabel, "button": playlistButton, "topWidget": containerWidget}

      # Add the containerWidget to the main ScrollableLayout
      self.scrollableAreaContainer.addWidget(containerWidget)

      count += 1