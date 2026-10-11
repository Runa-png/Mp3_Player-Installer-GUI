def songControl(self, index):
  # Flip the status of the button
  newStatus = not self.widgetList[index]["button"].clickedStatus
  self.widgetList[index]["button"].clickedStatus = newStatus

  # Update the button text
  if self.widgetList[index]["button"].clickedStatus:
    newText = "Remove"
    color = "rgb(200,0,0)"
    fontWeight = 900
  else:
    newText = "Add"
    color = "rgb(255,255,255)"
    fontWeight = 500
  self.widgetList[index]["button"].setText(newText)
  self.widgetList[index]["button"].setStyleSheet(f"color: {color}; font-size: 20px; background-color: {self.config.createPlaylistStackedWindow.add_Button_Color}; font-weight: {fontWeight}")
  
  artistName = self.widgetList[index]["artistName"]
  songName = self.widgetList[index]["songName"]
  songLocation = self.widgetList[index]["fileLocation"]
  albumName = self.widgetList[index]["albumName"]

  emittedData = {"artistName": artistName, "songName": songName, "songLocation": songLocation, "albumName": albumName}
  if newStatus == True:
    self.ADDSONG.emit(emittedData)
  else:
    self.REMOVESONG.emit(emittedData)
