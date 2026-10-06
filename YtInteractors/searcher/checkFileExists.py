def checkFileExists(location):
  try:
    open(location)
  except FileNotFoundError:
    return {"status": False, "reason": "File does not exist"}
  except PermissionError:
    return {"status": False, "reason": "No permissions to see file"}
  
  return {"status": True}
