def urlFormatter(urlList: list):
  for url in urlList:
    url["url"] = "https://www.youtube.com/watch?v=" + url["url"]
  return urlList