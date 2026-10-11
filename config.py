class configs:
  class MainWindow:
    leftSection = "rgb(15,15,30)"
    middleSection = "rgb(25,25,50)"
    rightSection = "rgb(15,15,30)"
    bottomSection = "rgb(50,50,75)"
  
  class ShuffleButton:
    width = 50
    clickedColor = "rgb(90,90,150)" # I'd recommed making this color a derivative from rightSection
    defaultColor = "rgb(45,45,75)" # I'd recommed making this color the same as other buttons ID1
  
  class Downloader:
    output = "music" # Change this to change where the music gets output to
    background_color = "rgb(45,45,75)" # I'd recommed making this color the same as other buttons ID1
    width = 50

  class CreatePlaylist:
    background_color = "rgb(45,45,75)" # I'd recommed making this color the same as other buttons ID1
    width = 50
    musicLocation = "music" # Where should the app look for mp3s
  
  class downloadWidget:
    inputHeight = 30
    song_background_color = "rgb(15,15,30)"

    middle_section = "rgb(30,30,70)"
    scrollable_area_color = "rgb(25,25,50)"
  
  class downloadSettingsWindow:
    background_color = "rgb(50,50,100)"
    main_layout_color = "rgb(25,25,50)"
  
  class createPlaylistStackedWindow:
    background_color = "rgb(10,10,30)"
    song_Widget_Background_color = "rgb(15,15,40)"
    add_Button_Color = "rgb(20,20,50)"
  
  class toolTip:
    text_color = "rgb(255,255,255)"
    background_color = "rgb(50,50,100)"
    font_size = 20
