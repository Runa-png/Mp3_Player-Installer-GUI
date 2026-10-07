from PyQt6.QtWidgets import (
  QMainWindow,
  QApplication,
  QWidget,
  QGridLayout,
  QVBoxLayout,
  QHBoxLayout,
  QToolBar,
  QStackedWidget
)

from PyQt6.QtCore import (
  Qt,
  QPropertyAnimation,
  QEasingCurve,
  QRunnable,
  QThreadPool,
  pyqtSlot,
  pyqtSignal,
  QObject
)

from PyQt6.QtGui import (
  QFontDatabase
)

from config import configs
import sys
from math import floor
from initialise import initialise
import shutil

from widgets.middleSection.createPlaylistWidget import CreatePlaylistWidget
from widgets.middleSection.downloadMusicWidget import DownloadMusicWidget

from widgets.rightSection.shuffleButton import ShuffleButton
from widgets.rightSection.createPlaylist import CreatePlaylistButton
from widgets.rightSection.downloadButton import DownloadButton

from YtInteractors.workers.searchingWorker import fetchFileWorker
from YtInteractors.workers.downloadingWorker import downloadFileWorker

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    config = configs()
    self.setContentsMargins(0,0,0,0)

    # Fonts
    fontId = QFontDatabase.addApplicationFont("AtkynsonMonoNerdFont-Regular.otf")
    fontFamily = QFontDatabase.applicationFontFamilies(fontId)

    # Central Widget
    central = QWidget()
    central.setStyleSheet(f"font-family: {fontFamily}")
    self.setCentralWidget(central)

    # 3 Column grid
    grid = QGridLayout(central)
    grid.setSpacing(0)
    grid.setContentsMargins(0,0,0,0)

    # -----------
    # LEFT COLUMN
    # -----------

    leftColumn = QWidget()
    leftColumn.setContentsMargins(0,0,0,0)
    leftColumn.setStyleSheet(f"background-color: {config.MainWindow.leftSection}")
    leftLayout = QVBoxLayout(leftColumn)
    
    # -------------
    # MIDDLE COLUMN
    # -------------

    self.middleColumn = QWidget()
    self.middleColumn.setContentsMargins(0,0,0,0)
    self.middleColumn.setStyleSheet(f"background-color: {config.MainWindow.middleSection}")

    self.middleLayout = QVBoxLayout(self.middleColumn)
    self.middleLayout.setContentsMargins(0,0,0,0)

    self.stackedWidget = QStackedWidget()

    self.playlistCreation = CreatePlaylistWidget()
    
    self.musicDownload = DownloadMusicWidget()
    self.musicDownload.SEARCHPRESSED.connect(lambda status: self.findAudioFunction(status))
    self.musicDownload.DOWNLOADPRESSED.connect(lambda data: self.downloadAudioFunction(data))
    
    self.stackedWidget.addWidget(self.playlistCreation)
    self.stackedWidget.addWidget(self.musicDownload)
    self.stackedWidget.setCurrentIndex(0)

    self.middleLayout.addWidget(self.stackedWidget)

    # ------------
    # RIGHT COLUMN
    # ------------

    self.rightColumn = QWidget()
    self.rightColumn.setStyleSheet(f"background-color: {config.MainWindow.rightSection}")

    # Vertical widget to store the buttons
    self.rightLayout = QVBoxLayout(self.rightColumn)
    self.rightLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
    self.rightLayout.setContentsMargins(0,0,0,0)

    # Shuffle playlist button
    self.shuffleButton = ShuffleButton()
    self.shuffleButton.SHUFFLE.connect(lambda status: print(status))
    self.rightLayout.addWidget(self.shuffleButton)

    # Create playlist button
    def playlistButtonPressed(self):
      self.stackedWidget.setCurrentIndex(0)
      self.playlistCreation.readMusic()
    
    self.createPlaylistButton = CreatePlaylistButton()
    self.createPlaylistButton.CREATEPRESSED.connect(lambda: playlistButtonPressed(self))
    self.rightLayout.addWidget(self.createPlaylistButton)

    # Download button
    self.downloadButton = DownloadButton()
    self.downloadButton.DOWNLOADPRESSED.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    self.rightLayout.addWidget(self.downloadButton)
  
    # ------
    # BOTTOM
    # ------

    self.bottomRow = QWidget()
    self.bottomRow.setStyleSheet(f"background-color: {config.MainWindow.bottomSection}")
    self.bottomRowLayout = QHBoxLayout(self.bottomRow)
    self.bottomRowLayout.setContentsMargins(0,0,0,0)

    # -----------
    # ADD LAYOUTS
    # -----------

    paddingTop = QWidget()
    paddingTop.setStyleSheet(f"background-color: {config.MainWindow.bottomSection}")
    grid.addWidget(paddingTop, 0,0,1,3)

    grid.addWidget(leftColumn, 1, 0)
    grid.addWidget(self.middleColumn, 1, 1)
    grid.addWidget(self.rightColumn, 1, 2)
    grid.addWidget(self.bottomRow, 2,0,1,3)

    grid.setColumnStretch(0,0)
    grid.setColumnStretch(1,1)
    grid.setColumnStretch(2,0)

    grid.setRowStretch(0,5) # Top row
    grid.setRowStretch(1,85) # Middle Row
    grid.setRowStretch(2,10) # Bottom row

    # --------------
    # MULTITHREADING
    # --------------

    self.threadPool = QThreadPool()
    self.threadRunning = False

    # ---------
    # VARIABLES 
    # ---------

    self.playlist = {}
  
  # Executes when the app has finished searching
  def finishedRunning(self, text):
    self.threadRunning = False
    self.musicDownload.statusLabel.setText(text)

  def findAudioFunction(self, data):
    # Terminate if user has already started the search
    if self.threadRunning == True:
      self.musicDownload.statusLabel.setText("Already running the download!")
      return
    
    self.threadRunning = True
    self.musicDownload.statusLabel.setText("")
    
    self.worker = fetchFileWorker(data)
    self.musicDownload.purgeSongs() # Clear the window of the last download

    self.worker.signals.STATUS.connect(lambda status: self.musicDownload.statusLabel.setText(status))
    self.worker.signals.URL_FOUND.connect(lambda status: self.musicDownload.addSong(status))
    self.worker.signals.FINISHED.connect(lambda: self.finishedRunning(""))
    self.worker.signals.UPDATE_PROGRESS.connect(lambda value: self.musicDownload.progressBar.setValue(value))
    
    self.threadPool.start(self.worker)

  def downloadAudioFunction(self, data):
    # Terminate if user has already started the search
    if self.threadRunning == True:
      self.musicDownload.statusLabel.setText("Already running the download!")
      return
    
    self.threadRunning = True
    self.musicDownload.statusLabel.setText("")
    self.musicDownload.progressBar.setValue(0)

    self.worker = downloadFileWorker(data)

    # Signals Recieved
    self.worker.signals.STATUS.connect(lambda status: self.musicDownload.statusLabel.setText(status))
    self.worker.signals.FINISHED.connect(lambda: self.finishedRunning(""))
    self.worker.signals.UPDATE_PROGRESS.connect(lambda data: self.downloadSuccessful(data[1], data[0]))
    self.worker.signals.FAILED_DOWNLOAD.connect(lambda index: self.downloadFailed(index))

    self.threadPool.start(self.worker)

  def downloadFailed(self, index):
    self.musicDownload.songWidgetList[index].title.setStyleSheet(
      "color: rgb(100, 0, 0); font-size: 20px"
    )
  def downloadSuccessful(self, index, value):
    self.musicDownload.progressBar.setValue(value)
    self.musicDownload.songWidgetList[index].title.setStyleSheet(
      "color: rgb(0, 100, 0); font-size: 20px"
    )
  
  # Executes when the window closes
  def closeEvent(self, event):
    if hasattr(self, "worker"):
      self.worker.stopEvent = True

    self.threadPool.clear()
    print("Please wait for the threads to clear!")

    event.accept()
    QApplication.quit()

if __name__ == "__main__":
  initialise()
  shutil.rmtree("cache", ignore_errors=True)

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  app.exec()