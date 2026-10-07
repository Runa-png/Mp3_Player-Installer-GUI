def songControl(self, index):
  print(self.widgetList[index])
  
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
  
  print(newStatus)
