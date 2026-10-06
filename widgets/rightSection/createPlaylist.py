from PyQt6.QtWidgets import (
  QPushButton,
  QWidget,
  QHBoxLayout
)

from PyQt6.QtCore import (
  QSize,
  pyqtSignal
)

from PyQt6.QtGui import (
  QIcon
)

from config import configs

class CreatePlaylistButton(QWidget):
  CREATEPRESSED = pyqtSignal()
  
  def __init__(self):
    config = configs()
    super().__init__()

    width = config.CreatePlaylist.width

    self.topLayout = QHBoxLayout(self)
    self.topLayout.setContentsMargins(0, 0, 0, 0)

    self.createPlaylistButton = QPushButton()
    
    self.createPlaylistButton.setIcon(QIcon("assets/create.png"))
    self.createPlaylistButton.setIconSize(QSize(width,width))
    self.createPlaylistButton.setFixedSize(QSize(width,width))

    self.createPlaylistButton.clicked.connect(self.CREATEPRESSED.emit)

    self.createPlaylistButton.setStyleSheet(f"background-color: {config.CreatePlaylist.background_color}; border: none; border-radius: 10px")

    self.topLayout.addWidget(self.createPlaylistButton)