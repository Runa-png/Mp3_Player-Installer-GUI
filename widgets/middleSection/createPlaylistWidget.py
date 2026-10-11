from PyQt6.QtWidgets import (
  QPushButton,
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QScrollArea,
  QLineEdit,
  QComboBox
)

from PyQt6.QtCore import (
  Qt,
  QSize,
  pyqtSignal
)

from PyQt6.QtGui import (
  QIcon,
  QPixmap
)

from PlaylistInteractions.songController import songControl
from PlaylistInteractions.calculateAccuracy import calculateAccuracy

from YtInteractors.searcher.getAlbumImage import getAlbumImage

from config import configs
import os
import sqlite3
import shutil
import operator

class CreatePlaylistWidget(QWidget):
  ADDSONG = pyqtSignal(dict)
  REMOVESONG = pyqtSignal(dict)
  CREATEPLAYLIST = pyqtSignal()
  
  def __init__(self):
    super().__init__()

    self.setContentsMargins(0,0,0,0)
    self.config = configs()

    topLayout = QVBoxLayout(self)
    self.titleLabel = QLabel("Create Playlist")
    self.titleLabel.setStyleSheet("color: white; font-size: 25px; font-weight: 900; text-decoration: underline")

    # Search Bar
    widgetHeight = 40
    
    self.playlistInteractionsWidget = QWidget()
    self.playlistInteractionsWidget.setContentsMargins(0,0,0,0)
    self.playlistInteractionsLayout = QHBoxLayout(self.playlistInteractionsWidget)
    self.playlistInteractionsLayout.setContentsMargins(0,0,0,0)

    self.playlistName = QLineEdit()
    self.playlistName.setFixedHeight(widgetHeight)
    self.playlistName.setPlaceholderText("Name of playlist")
    self.playlistName.setStyleSheet("color: white; font-size: 20px")

    self.createPlaylistButton = QPushButton("Create!")
    self.createPlaylistButton.setFixedHeight(widgetHeight)
    self.createPlaylistButton.setStyleSheet("color: white; font-size: 20px")
    self.createPlaylistButton.setMinimumWidth(120)
    self.createPlaylistButton.clicked.connect(lambda: self.CREATEPLAYLIST.emit())

    self.playlistInteractionsLayout.addWidget(self.playlistName)
    self.playlistInteractionsLayout.addWidget(self.createPlaylistButton)
    
    searchBarWidget = QWidget()
    searchBarWidget.setFixedHeight(widgetHeight)
    searchBarWidget.setContentsMargins(0,0,0,0)
    searchBarLayout = QHBoxLayout(searchBarWidget)
    searchBarLayout.setContentsMargins(0,0,0,0)

    searchDropdown = QComboBox()
    searchDropdown.setFixedHeight(widgetHeight)
    searchDropdown.setMinimumWidth(120)
    searchDropdown.setStyleSheet("font-size: 20px; color: white")
    searchDropdown.addItem("Title")
    searchDropdown.addItem("Artist")
    searchDropdown.addItem("Album")
    
    searchBar = QLineEdit()
    searchBar.setPlaceholderText(f"Name of {searchDropdown.currentText()}")
    searchDropdown.currentTextChanged.connect(lambda: searchBar.setPlaceholderText(f"Name of {searchDropdown.currentText()}"))
    searchBar.setFixedHeight(widgetHeight)
    searchBar.setStyleSheet("font-size: 20px; color: white")
    searchBar.editingFinished.connect(lambda: self.searchCompleted())

    self.queryWidgets = {"searchBar": searchBar, "searchDropdown": searchDropdown}

    searchBarLayout.addWidget(searchBar)
    searchBarLayout.addWidget(searchDropdown)

    scrollableArea = QScrollArea()
    scrollableArea.setStyleSheet("border: none")
    scrollableArea.setWidgetResizable(True)
    
    scrollableAreaContainerWidget = QWidget()
    self.scrollableAreaContainer = QVBoxLayout(scrollableAreaContainerWidget)

    scrollableArea.setWidget(scrollableAreaContainerWidget)

    scrollableAreaContainerWidget.setStyleSheet(f"background-color: {self.config.createPlaylistStackedWindow.background_color}; border-radius: 20px")
    
    topLayout.addWidget(self.titleLabel, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    topLayout.addWidget(self.playlistInteractionsWidget)
    topLayout.addWidget(searchBarWidget)
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
        print("File extension incorrect")
        continue

      data = cursor.execute("SELECT * FROM songs WHERE location = ?", (location,)).fetchone()

      title = data[0]
      artist = data[1]
      artLocation = data[3]
      albumName = data[4]
      
      newDataDict = {"title": title, "artist": artist, "location": location, "albumArt": artLocation, "albumName": albumName}
      songDataList.append(newDataDict)
    
    self.widgetList = {}

    length = len(songDataList)
    count = 0
    widgetHeight = 160
    # Iterate over each song in the list
    
    for songDict in songDataList:
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
      nameLabel.setStyleSheet("color: rgb(255,255,255); font-size: 25px")
      
      artistLabel = QLabel(songDict["artist"])
      artistLabel.setStyleSheet("color: rgb(150,150,150); font-size: 20px")

      albumLabel = QLabel(songDict["albumName"])
      albumLabel.setStyleSheet("color: rgb(100,100,100); font-size: 15px")

      informationLayout.addStretch()
      informationLayout.addWidget(nameLabel, alignment = Qt.AlignmentFlag.AlignBottom)
      informationLayout.addWidget(artistLabel, alignment = Qt.AlignmentFlag.AlignBottom)
      informationLayout.addWidget(albumLabel, alignment = Qt.AlignmentFlag.AlignBottom)

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
      iconLabel.setPixmap(icon.pixmap(150,150))
      iconLabel.setStyleSheet("border-radius: 15px")

      # Add widgets to the indexed dict
      self.widgetList[count] = {
        "name": nameLabel,
        "artist": artistLabel,
        "button": playlistButton,
        "topWidget": containerWidget,
        "fileLocation": songDict["location"],
        "albumName": songDict["albumName"],
        "songName": songDict["title"],
        "artistName": songDict["artist"]
      }

      containerLayout.addWidget(iconLabel)
      containerLayout.addWidget(informationWidget, alignment = Qt.AlignmentFlag.AlignLeft, stretch=1)
      containerLayout.addWidget(playlistButtonContainer, alignment = Qt.AlignmentFlag.AlignRight)

      # Use this for clicked status
      playlistButton.clickedStatus = False

      # Add the song to the internal playlist
      playlistButton.clicked.connect(lambda _, index=count: songControl(self, index))

      count += 1
    
    unsortedDataList = []
    # Remove the indexes
    for index in self.widgetList:
      data = self.widgetList[index]
      unsortedDataList.append(data)
    
    # Sort the widgetlist by album
    sortedDataList = sorted(unsortedDataList, key=lambda item: item["albumName"].casefold())
    (len(sortedDataList))

    for sortedItem in sortedDataList:
      # Add the containerWidget to the main ScrollableLayout
      self.scrollableAreaContainer.addWidget(sortedItem["topWidget"])

  def purgeWidgets(self):
    for index in self.widgetList:
      widget = self.widgetList[index]["topWidget"]
      self.scrollableAreaContainer.removeWidget(widget)
      widget.setParent(None)
    self.widgetList = {}
  
  def reload(self):
    self.purgeWidgets() # Remove Widgets
    self.readMusic() # Add new iteration of widgets
  
  def searchCompleted(self):    
    query = self.queryWidgets["searchBar"].text()
    key = self.queryWidgets["searchDropdown"].currentText()

    unsortedAccuracyList = []
    for index in self.widgetList:
      accuractDict = calculateAccuracy(data = self.widgetList[index], comparison = query, dictKey = key)
      unsortedAccuracyList.append(accuractDict)
    sortedAccuracyList = sorted(unsortedAccuracyList, key=lambda item: item["accuracy"], reverse=True)

    self.purgeWidgets()

    count = 0
    for widget in sortedAccuracyList:
      self.scrollableAreaContainer.addWidget(widget["topWidget"])
      
      self.widgetList[count] = (widget)
      count += 1