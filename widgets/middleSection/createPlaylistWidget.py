from PyQt6.QtWidgets import (
  QPushButton,
  QWidget,
  QVBoxLayout,
  QLabel
)

from PyQt6.QtCore import (
  Qt,
  QSize
)

from PyQt6.QtGui import (
  QIcon
)

from config import configs

class CreatePlaylistWidget(QWidget):
  def __init__(self):
    super().__init__()

    self.setContentsMargins(0,0,0,0)

    topLayout = QVBoxLayout(self)
    label = QLabel("Create Playlist")
    label.setStyleSheet("color: white; font-size: 25px; font-weight: 900; text-decoration: underline")

    topLayout.addWidget(label, alignment = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)