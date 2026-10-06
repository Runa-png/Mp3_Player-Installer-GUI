from .readCSV import readCSV

def fileDataFetching(info: dict):
  if info["option"] == "CSV":
    data = readCSV(info["location"])
  else:
    return {"status": False, "reason": "Feature not implemented"}

  if data["status"] == False:
    return data
  
  # Filter required columns
  CSV = data["csv"][["Song", "Artist"]]
  
  return {"status": True, "csv": CSV}
