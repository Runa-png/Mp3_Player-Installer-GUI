from PyQt6.QtCore import (
  Qt,
  QRunnable,
  pyqtSlot,
  pyqtSignal,
  QObject
)

from ..searcher.fileDataFetching import fileDataFetching
from ..searcher.getUrl import getVideoUrl

from math import floor

class fetchFileWorker(QRunnable):
  class WorkerSignals(QObject):
    STATUS = pyqtSignal(str)
    URL_FOUND = pyqtSignal(dict)
    FINISHED = pyqtSignal()
    UPDATE_PROGRESS = pyqtSignal(int)
  
  def __init__(self, data):
    super().__init__()
    self.data = data
    self.stopEvent = False
    self.signals = self.WorkerSignals()
  
  @pyqtSlot()
  def run(self):
    dataframe = fileDataFetching(self.data)
    
    largestCount = len(dataframe["csv"])
    startCount = 0
    
    self.signals.UPDATE_PROGRESS.emit(0)

    if dataframe["status"] == False:
      self.signals.STATUS.emit(dataframe["reason"])
      self.signals.FINISHED.emit()
      return
    self.signals.STATUS.emit("")

    for index, row in dataframe["csv"].iterrows():
      if self.stopEvent:
        return
      getVideoUrl(self, row, index)
      
      startCount += 1
      percentage = floor((startCount / largestCount) * 100)
      self.signals.UPDATE_PROGRESS.emit(percentage)
    
    self.signals.FINISHED.emit()