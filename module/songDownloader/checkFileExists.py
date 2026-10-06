def checkFileExists(location: str):
  try:
    with open(location):
      return {"success": True}
  except FileNotFoundError:
    return {"success": False, "message": "File was not found"}
  except PermissionError:
    return {"success": False, "message": "Insufficient permissions to access folder"}