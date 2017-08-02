import requests
from lib import ece


def check_wrong_password_from_regular_client(url, user):
  response = requests.get(url, auth=(user, "wrong password"))
  assert response.status_code == 401
  assert "WWW-Authenticate" in response.headers


def check_wrong_password_from_xhr_client(url, user):
  headers = {
    "X-Requested-With": "XMLHttpRequest"
  }

  response = requests.get(url, auth=(user, "wrong password"), headers=headers)
  assert response.status_code == 401
  assert "WWW-Authenticate" not in response.headers


def check_wrong_password_from_xhr_client_no_auth(url, user):
  headers = {
    "X-Requested-With": "XMLHttpRequest"
  }

  response = requests.get(url, headers=headers)
  assert response.status_code == 401
  assert "WWW-Authenticate" in response.headers


def check(ws_base_url, publication, user):
  ece.create_publication(publication)
  url = ws_base_url + "/index.xml"
  check_wrong_password_from_regular_client(url, user)
  check_wrong_password_from_xhr_client(url, user)
  check_wrong_password_from_xhr_client_no_auth(url, user)
