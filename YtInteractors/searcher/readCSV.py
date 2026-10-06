import pandas as pd 

from .checkFileExists import checkFileExists

def readCSV(location):
  fileExists = checkFileExists(location)

  if fileExists["status"] == False:
    return fileExists

  # fetch and filter required columns
  csv = pd.read_csv(location)

  return {"status": True, "csv": csv}