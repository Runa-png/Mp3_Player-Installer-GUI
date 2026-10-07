import sqlite3

def initialise():
  connection = sqlite3.connect("database.db")
  cursor = connection.cursor()

  # Create tables
  cursor.execute("CREATE TABLE IF NOT EXISTS songs (name, artist, location, albumArt)")

  connection.commit()
  connection.close()