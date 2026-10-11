from PyQt6.QtWidgets import (
  QPushButton,
  QWidget,
  QVBoxLayout,
  QHBoxLayout,
  QLabel,
  QLineEdit,
  QComboBox,
  QProgressBar,
  QScrollArea
)

from PyQt6.QtCore import (
  Qt,
  QSize,
  pyqtSignal
)

from PyQt6.QtGui import (
  QIcon
)

from config import configs
from math import floor

from ..windows.downloadSettingsWindow import DownloadSettingsWindow

class DownloadMusicWidget(QWidget):  
  SEARCHPRESSED = pyqtSignal(dict)
  DOWNLOADPRESSED = pyqtSignal(dict)
  
  def __init__(self):
    config = configs()
    super().__init__()

    self.setContentsMargins(0,0,0,0)

    topLayout = QVBoxLayout(self)
    
    # ---------
    # ALIGN TOP
    # ---------

    alignTop = QVBoxLayout()
    alignTop.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
    
    self.label = QLabel("Download Music")
    self.label.setContentsMargins(0,0,0,0)
    self.label.setStyleSheet("color: white; font-size: 25px; font-weight: 900; text-decoration: underline")

    searchWidget = QWidget()
    searchLayout = QHBoxLayout(searchWidget)
    
    # Global Height for search bar
    height = config.downloadWidget.inputHeight
    
    # Input for file location
    self.searchBar = QLineEdit()
    self.searchBar.setPlaceholderText("Enter file location / Youtube URL")
    self.searchBar.setStyleSheet("color: white")
    self.searchBar.isClearButtonEnabled = True
    self.searchBar.setMinimumHeight(height)
    searchLayout.addWidget(self.searchBar)

    # Button to search the file location
    self.searchButton = QPushButton("Search")
    self.searchButton.setMinimumHeight(height)
    self.searchButton.setStyleSheet("color: white; font-size: 15px")
    searchLayout.addWidget(self.searchButton)

    # Selection for what type of file you are using
    self.dropdown = QComboBox()
    self.dropdown.setStyleSheet("color: white; font-size: 15px")
    self.dropdown.setMinimumHeight(height)
    self.dropdown.addItem("CSV")
    self.dropdown.addItem("URL")
    searchLayout.addWidget(self.dropdown)

    # Button to commit to the download
    self.downloadButton = QPushButton("Download")
    self.downloadButton.setMinimumHeight(height)
    self.downloadButton.setStyleSheet("color: white; font-size: 15px")
    searchLayout.addWidget(self.downloadButton)

    alignTop.addWidget(self.label, alignment = Qt.AlignmentFlag.AlignCenter)
    alignTop.addSpacing(40)
    alignTop.addWidget(searchWidget)

    topLayout.addLayout(alignTop)

    self.searchButton.clicked.connect(lambda: self.SEARCHPRESSED.emit({"location": self.searchBar.text(), "option": self.dropdown.currentText()}))
    self.downloadButton.clicked.connect(lambda: self.DOWNLOADPRESSED.emit(self.songData))

    # ------------
    # ALIGN CENTER
    # ------------

    self.alignCenterWidget = QWidget()
    self.alignCenter = QVBoxLayout(self.alignCenterWidget)

    self.statusLabel = QLabel()
    self.statusLabel.setStyleSheet("color: white; font-size: 20px; font-weight: 900")

    # Song Download Section
    self.songWidget = QWidget()
    self.songList = QVBoxLayout()
    self.songWidget.setLayout(self.songList)

    self.songWidget.setStyleSheet(f"background-color: {config.downloadWidget.middle_section}")

    self.progressBar = QProgressBar()

    self.songList.addWidget(self.progressBar, alignment = Qt.AlignmentFlag.AlignTop)

    self.songStorageWidget = QWidget()
    self.songStorageWidget.setStyleSheet(f"background-color: {config.downloadWidget.scrollable_area_color}")
    
    self.songStorageLayout = QVBoxLayout(self.songStorageWidget)

    # Guide Columns
    guideWidget = QWidget()
    guideLayout = QHBoxLayout(guideWidget)
    
    nameLabel = QLabel("Name")
    nameLabel.setStyleSheet("color: white; font-size: 20px")
    guideLayout.addWidget(nameLabel, alignment = Qt.AlignmentFlag.AlignCenter)

    artistLabel = QLabel("Artist")
    artistLabel.setStyleSheet("color: white; font-size: 20px")
    guideLayout.addWidget(artistLabel, alignment = Qt.AlignmentFlag.AlignCenter)

    accuracyLabel = QLabel("Accuracy")
    accuracyLabel.setStyleSheet("color: white; font-size: 20px")
    guideLayout.addWidget(accuracyLabel, alignment = Qt.AlignmentFlag.AlignCenter)

    guideLayout.addWidget(QLabel("")) # Just for padding
    self.songList.addWidget(guideWidget)

    self.songStorage = QScrollArea()
    self.songStorage.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.songStorage.setWidgetResizable(True)

    self.songStorage.setWidget(self.songStorageWidget)

    self.songList.addWidget(self.songStorage, stretch=1)

    self.songWidgetList = {}
    self.songData = {}
    ##

    self.alignCenter.addWidget(self.songWidget, stretch = 1)
    self.alignCenter.addWidget(self.statusLabel, alignment = Qt.AlignmentFlag.AlignCenter)

    topLayout.addWidget(self.alignCenterWidget, stretch=1)

  def addSong(self, data):
    config = configs()
    
    songWidget = QWidget()
    fixedHeight = 100
    songWidget.setFixedHeight(fixedHeight)
    songWidget.setStyleSheet(f"background-color: {config.downloadWidget.song_background_color}")
    songLayout = QHBoxLayout()
    songLayout.setContentsMargins(0,0,0,0)
    
    songWidget.title = QLabel(data["name"][:20])
    songWidget.title.setStyleSheet("color: white; font-size: 20px")

    songWidget.artist = QLabel(data["artist"][:20])
    songWidget.artist.setStyleSheet("color: white; font-size: 20px")

    songWidget.accuracy = QLabel(str(floor(data["ratio"])) + "%")
    songWidget.accuracy.setStyleSheet("color: white; font-size: 20px")
    
    index = data["index"]

    self.songData[index] = {"title": data["name"], "artist": data["artist"], "url": data["id"], "confidence": data["confident"], "CSVArtist": data["CSVArtist"], "albumUrl": data["albumImageLocation"], "albumName": data["albumName"]}

    songWidget.buttonsWidget = QWidget()
    buttonsLayout = QHBoxLayout(songWidget.buttonsWidget)
    buttonsLayout.setContentsMargins(0, 0, 0, 0)
    
    removeButton = QPushButton("Delete")
    removeButton.setFixedHeight(fixedHeight)
    removeButton.setStyleSheet("color: white; font-size: 15px; font-weight:900")
    removeButton.setContentsMargins(0,0,0,0)
    removeButton.clicked.connect(lambda: self.removeSong(index))

    settingsButton = QPushButton("Controls")
    settingsButton.setFixedHeight(fixedHeight)
    settingsButton.setStyleSheet("color: white; font-size: 15px; font-weight:900")
    settingsButton.setContentsMargins(0,0,0,0)
    settingsButton.clicked.connect(lambda: self.settingsPage(index))

    buttonsLayout.addWidget(removeButton)
    buttonsLayout.addWidget(settingsButton)

    songLayout.addWidget(songWidget.title, alignment = Qt.AlignmentFlag.AlignCenter)
    songLayout.addWidget(songWidget.artist, alignment = Qt.AlignmentFlag.AlignCenter)
    songLayout.addWidget(songWidget.accuracy, alignment = Qt.AlignmentFlag.AlignCenter)
    songLayout.addWidget(songWidget.buttonsWidget)

    songWidget.setLayout(songLayout)

    self.songWidgetList[index] = songWidget

    self.songStorageLayout.addWidget(songWidget)
  
  def removeSong(self, index):
    widget = self.songWidgetList.pop(index, None)

    if widget is None:
      return

    self.songData.pop(index, None)
    self.songStorageLayout.removeWidget(widget)
    widget.deleteLater()
  
  def purgeSongs(self):
    for widget in self.songWidgetList.values():
      self.songStorageLayout.removeWidget(widget)
      widget.deleteLater()

    self.songData = {}
    self.songWidgetList.clear()
  
  def settingsPage(self, index):
    self.settingsWindow = DownloadSettingsWindow(self, index)
    self.settingsWindow.show()
