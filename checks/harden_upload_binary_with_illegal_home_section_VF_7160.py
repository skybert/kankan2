import requests
from lxml import etree
from lib import ece
from io import StringIO


def check(ws_base_url, publication, content_type, user, password):
  ece.create_publication(publication)
  result = {"success": 0, "error": 0, "messages": []}
  url = ws_base_url \
      + "/publication/" + publication \
      + "/binary/" + content_type \
      + "?Name=foo.jpg"

  auth = (user, password)
  fn = "/tmp/picture.jpg"

  section_uri = ws_base_url + "/escenic/section/48"
  check_valid_section(url, auth, fn, section_uri)

  section_uri = ws_base_url + "/escenic/section/29"
  check_invalid_section_belongs_to_other_pub(url, auth, fn, section_uri)

  return result


def check_valid_section(url, auth, fn, section_uri):
  headers = {
    "X-Escenic-media-filename": fn[fn.rfind("/"):],
    "X-Escenic-home-section-uri": section_uri,
    "Content-type": "image/jpeg"
  }

  with open(fn, 'rb') as f:
    response = requests.post(url, auth=auth, data=f, headers=headers)

  assert response.status_code == 201
  assert "Location" in response.headers


def check_invalid_section_belongs_to_other_pub(url, auth, fn, section_uri):
  headers = {
    "X-Escenic-media-filename": fn[fn.rfind("/"):],
    "X-Escenic-home-section-uri": section_uri,
    "Content-type": "image/jpeg"
  }

  with open(fn, 'rb') as f:
    response = requests.post(url, auth=auth, data=f, headers=headers)
  assert response.text.index("doesn't belong to publication") != -1
  assert response.status_code == 400
