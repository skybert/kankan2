import requests


def check(conf):
  response = requests.get(conf["ece_admin_url"])
  assert response.status_code == 200
