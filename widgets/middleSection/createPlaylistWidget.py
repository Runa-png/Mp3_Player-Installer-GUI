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
  QIcon,
  QPixmap
)

from PlaylistInteractions.songController import songControl

from YtInteractors.searcher.getAlbumImage import getAlbumImage

from config import configs
import os
import sqlite3
import shutil

class CreatePlaylistWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.setContentsMargins(0,0,0,0)
    self.config = configs()

    topLayout = QVBoxLayout(self)
    titleLabel = QLabel("Create Playlist")
    titleLabel.setStyleSheet("color: white; font-size: 25px; font-weight: 900; text-decoration: underline")

    scrollableArea = QScrollArea()
    scrollableArea.setStyleSheet("border: none")
    scrollableArea.setWidgetResizable(True)
    
    scrollableAreaContainerWidget = QWidget()
    self.scrollableAreaContainer = QVBoxLayout(scrollableAreaContainerWidget)

    scrollableArea.setWidget(scrollableAreaContainerWidget)

    scrollableAreaContainerWidget.setStyleSheet(f"background-color: {self.config.createPlaylistStackedWindow.background_color}; border-radius: 20px")
    
    topLayout.addWidget(titleLabel, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    topLayout.addWidget(scrollableArea, stretch=1)

    # Just run the search function
    os.makedirs(self.config.CreatePlaylist.musicLocation, exist_ok=True)
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
      artLocation = data[3]
      
      newDataDict = {"title": title, "artist": artist, "location": location, "albumArt": artLocation}
      songDataList.append(newDataDict)
    
    self.widgetList = {}

    length = len(songDataList)
    count = 0
    widgetHeight = 160
    # Iterate over each song in the list
    for songDict in songDataList:
      print(songDict)

      containerWidget = QWidget()
      containerWidget.setFixedHeight(widgetHeight)
      containerWidget.setContentsMargins(0,0,0,0)
      containerWidget.setStyleSheet(f"background-color: {self.config.createPlaylistStackedWindow.song_Widget_Background_color}")
      containerLayout = QHBoxLayout(containerWidget)
      containerLayout.setContentsMargins(0,0,0,0)

      # Widgets to be in the layout
      
      # Artist name and song name
      informationContainer = QScrollArea()
      informationContainer.setStyleSheet("border: none")
      informationContainer.setWidgetResizable(True)
      
      informationWidget = QWidget()
      informationLayout = QVBoxLayout(informationWidget)

      nameLabel = QLabel(songDict["title"])
      nameLabel.setStyleSheet("color: rgb(255,255,255); font-size: 20px")
      
      artistLabel = QLabel(songDict["artist"])
      artistLabel.setStyleSheet("color: rgb(150,150,150); font-size: 15px")

      informationLayout.addStretch()
      informationLayout.addWidget(nameLabel, alignment = Qt.AlignmentFlag.AlignBottom)
      informationLayout.addWidget(artistLabel, alignment = Qt.AlignmentFlag.AlignBottom)

      playlistButtonContainer = QWidget()
      playlistButtonContainer.setFixedWidth(150)
      playlistButtonLayout = QVBoxLayout(playlistButtonContainer)
      playlistButtonLayout.setContentsMargins(0,0,0,0)
      playlistButton = QPushButton("Add")
      playlistButton.setStyleSheet(f"color: white; font-size:20px; background-color: {self.config.createPlaylistStackedWindow.add_Button_Color}")
      playlistButton.setFixedHeight(widgetHeight)
      playlistButton.setContentsMargins(0,0,0,0)
      playlistButtonLayout.addWidget(playlistButton)
      
      # Image
      icon = getAlbumImage(songDict["location"])
      iconLabel = QLabel()
      iconLabel.setPixmap(icon.pixmap(300,300))



      # Add widgets to the indexed dict
      self.widgetList[count] = {"name": nameLabel, "artist": artistLabel, "button": playlistButton, "topWidget": containerWidget}

      containerLayout.addWidget(iconLabel)
      containerLayout.addWidget(informationWidget)
      containerLayout.addWidget(playlistButtonContainer, alignment = Qt.AlignmentFlag.AlignRight)
      
      # nameContainer = QScrollArea()
      # nameContainer.setStyleSheet("border: none")
      # nameContainer.setWidgetResizable(True)
      # nameLabel = QLabel(songDict["title"])
      # nameLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
      # nameLabel.setStyleSheet("color: white; font-size:15px; padding-left: 20px")
      # nameContainer.setWidget(nameLabel)
      
      # artistContainer = QScrollArea()
      # artistContainer.setStyleSheet("border: none")
      # artistContainer.setWidgetResizable(True)
      # artistLabel = QLabel(songDict["artist"])
      # artistLabel.setAlignment(Qt.AlignmentFlag.AlignVCenter)
      # artistLabel.setStyleSheet("color: white; font-size:15px")
      # artistContainer.setWidget(artistLabel)

      # Use this for clicked status
      playlistButton.clickedStatus = False

      # Add the song to the internal playlist
      playlistButton.clicked.connect(lambda _, index=count: songControl(self, index))

      # Add the containerWidget to the main ScrollableLayout
      self.scrollableAreaContainer.addWidget(containerWidget)

      count += 1