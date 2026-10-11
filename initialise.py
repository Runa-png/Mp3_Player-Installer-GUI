import sqlite3

def initialise():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  # Create tables
  cursor.execute("CREATE TABLE IF NOT EXISTS songs (name, artist, location, albumArt, albumName)")
  cursor.execute("CREATE TABLE IF NOT EXISTS playlistId (id INTEGER PRIMARY KEY AUTOINCREMENT, tableName TEXT UNIQUE)")
  cursor.execute("CREATE TABLE IF NOT EXISTS playlists (playlistName TEXT, name TEXT, author TEXT, location TEXT, albumName TEXT, FOREIGN KEY (playlistName) REFERENCES playlistId(id) ON DELETE CASCADE)")

  connection.commit()
  connection.close()