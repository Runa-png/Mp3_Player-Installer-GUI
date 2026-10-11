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

class DownloadSettingsWindow(QWidget):
  def __init__(self, parent, index):
    config = configs()
    super().__init__()

    self.parentWindow = parent
    self.setFixedSize(QSize(500,500))
    self.setStyleSheet(f"background-color: {config.downloadSettingsWindow.background_color}")

    self.mainWidget = QWidget()
    self.mainWidget.setStyleSheet(f"background-color: {config.downloadSettingsWindow.main_layout_color}")
    self.mainLayout = QVBoxLayout(self.mainWidget)

    (str(self.parentWindow.songData[index]))

    data = self.parentWindow.songData[index]

    self.nameWidget = QWidget()
    self.nameWidget.setStyleSheet("color: white")
    self.nameLayout = QVBoxLayout(self.nameWidget)
    self.nameHint = QLabel("Song Name")
    self.nameHint.setStyleSheet("font-size: 24px; text-decoration: underline")
    self.nameLabel = QLabel(str(data["title"]))
    self.nameLabel.setStyleSheet("font-size: 22px")
    self.nameLayout.addWidget(self.nameHint, alignment = Qt.AlignmentFlag.AlignCenter)
    self.nameLayout.addWidget(self.nameLabel, alignment = Qt.AlignmentFlag.AlignCenter)
    
    self.artistWidget = QWidget()
    self.artistWidget.setStyleSheet("color: white")
    self.artistLayout = QVBoxLayout(self.artistWidget)
    self.artistHint = QLabel("Artist Name")
    self.artistHint.setStyleSheet("font-size: 24px; text-decoration: underline")
    self.artistLabel = QLabel(str(data["artist"]))
    self.artistLabel.setStyleSheet("font-size: 22px")
    self.artistLayout.addWidget(self.artistHint, alignment = Qt.AlignmentFlag.AlignCenter)
    self.artistLayout.addWidget(self.artistLabel, alignment = Qt.AlignmentFlag.AlignCenter)
    
    self.urlWidget = QWidget()
    self.urlLayout = QHBoxLayout(self.urlWidget)
    self.urlArea = QLineEdit(str(data["url"]))
    self.urlArea.setStyleSheet("color: white")
    self.urlLayout.addWidget(self.urlArea)

    self.updateButtonWidget = QWidget()
    self.updateButtonLayout = QHBoxLayout(self.updateButtonWidget)
    self.updateButton = QPushButton("Update URL")
    self.updateButton.setStyleSheet("color: white; font-size: 17px")
    self.updateButton.setFixedHeight(40)
    self.updateButtonLayout.addWidget(self.updateButton)

    self.mainLayout.addWidget(self.nameWidget, alignment = Qt.AlignmentFlag.AlignCenter)
    self.mainLayout.addWidget(self.artistWidget, alignment = Qt.AlignmentFlag.AlignCenter)
    self.mainLayout.addWidget(self.urlWidget)
    self.mainLayout.addWidget(self.updateButtonWidget)

    self.windowLayout = QVBoxLayout(self)
    self.windowLayout.addWidget(self.mainWidget)

    self.updateButton.clicked.connect(lambda: self.updateURL(index, self.urlArea.text()))

  def updateURL(self, index, replacement):
    self.parentWindow.songData[index]["url"] = replacement
    
    songWidget = self.parentWindow.songWidgetList[index]
    songWidget.accuracy.setText("Updated")