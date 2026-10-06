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

class ShuffleButton(QWidget):
  SHUFFLE = pyqtSignal(bool)
  
  def __init__(self):
    super().__init__()

    self.config = configs()
    width = self.config.ShuffleButton.width

    self.mainLayout = QHBoxLayout(self)

    self.shuffleButton = QPushButton()
    self.shuffleButton.setContentsMargins(0,0,0,0)
    self.shuffleButton.setIcon(QIcon("assets/shuffle.png"))
    self.shuffleButton.setIconSize(QSize(width, width))
    self.shuffleButton.setFixedSize(QSize(width, width))

    self.shuffleButton.setStyleSheet(f"background-color: {self.config.ShuffleButton.defaultColor}; border: none; border-radius: 10px")

    self.shuffleButton.clicked.connect(self.buttonPressed)

    self.isPressed = False

    self.mainLayout.addWidget(self.shuffleButton)
  
  def buttonPressed(self):
    self.isPressed = not self.isPressed
    if self.isPressed:
      self.shuffleButton.setStyleSheet(f"background-color: {self.config.ShuffleButton.clickedColor}; border: none; border-radius: 10px")
    else:
      self.shuffleButton.setStyleSheet(f"background-color: {self.config.ShuffleButton.defaultColor}; border: none; border-radius: 10px")
    self.SHUFFLE.emit(self.isPressed)
