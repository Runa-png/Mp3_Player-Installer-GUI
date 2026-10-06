import pandas as pd 
from .checkFileExists import checkFileExists

def readCSV(location: str):
  # Check if file exists as a file
  fileExists = checkFileExists(location)
  if not fileExists["success"]:
    return {"status": False, "response": fileExists["message"]}
  
  # Check to see the file has content and has parsable rows
  try:
    csv = pd.read_csv(location)
  except pd.errors.EmptyDataError:
    return {"status": False, "response": "CSV file is empty!"}
  
  # Everything seems fine!
  # Tests executed with No file, Empty file, Full file
  return {"status": True, "response": csv}