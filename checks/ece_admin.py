from urllib import request

def check(url):
  result = {"success" : 0, "error": 0}
  try:
    response = request.urlopen(url)
    html = response.read()
    result["success"] += 1
  except:
    print("Failed GETing " + url)
    result["error"] += 1


  return result
