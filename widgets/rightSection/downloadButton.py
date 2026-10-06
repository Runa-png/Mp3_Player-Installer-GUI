from PyQt6.QtWidgets import (
  QWidget,
  QHBoxLayout,
  QPushButton
)

from PyQt6.QtCore import (
  QSize,
  pyqtSignal
)

from PyQt6.QtGui import (
  QIcon
)

from config import configs

class DownloadButton(QWidget):
  DOWNLOADPRESSED = pyqtSignal()
  
  def __init__(self):
    super().__init__()

    self.config = configs()
    width = self.config.Downloader.width

    self.mainLayout = QHBoxLayout(self)

    self.downloadButton = QPushButton()
    self.downloadButton.setContentsMargins(0,0,0,0)
    self.downloadButton.setIcon(QIcon("assets/download.png"))
    self.downloadButton.setIconSize(QSize(width, width))
    self.downloadButton.setFixedSize(QSize(width, width))

    self.downloadButton.clicked.connect(self.DOWNLOADPRESSED.emit)

    self.downloadButton.setStyleSheet(f"background-color: {self.config.Downloader.background_color}; border: none; border-radius: 10px")

    self.mainLayout.addWidget(self.downloadButton)
