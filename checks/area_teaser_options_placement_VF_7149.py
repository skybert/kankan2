import requests
from lxml import etree
from lib import ece
from io import StringIO


def check_changing_teaser_options(url, auth, doc, teaser_option_name):
  r = doc.xpath(
    "/atom:entry" +
    "/atom:content" +
    "/vdf:payload" +
    "/vdf:field[@name='page']" +
    "/vdf:value" +
    "/group:group" +
    "/group:area[@name='main']" +
    "/group:group" +
    "/vdf:payload" +
    "/vdf:field[@name='" + teaser_option_name + "']" +
    "/vdf:value",
    namespaces=ece.xml_namespaces)

  # Change the options no matter what they are
  for el in r:
    if el.text == "s":
      el.text = "m"
    elif el.text == "m":
      el.text = "l"
    elif el.text == "l":
      el.text = "s"

  # print("teaser_option_name=" + teaser_option_name)
  # print(etree.tostring(doc))

  headers = {
    "Content-type": "application/atom+xml; type=entry",
    "If-Match": "*"
  }

  response = requests.put(
    url,
    data=etree.tostring(doc),
    auth=auth,
    headers=headers
  )

  assert response.status_code == 204

  # Now, pull down the section page document again and check its
  # teaser options
  response = requests.get(url, auth=auth)
  doc = etree.parse(StringIO(response.text))
  check_teaser_options(doc, teaser_option_name)


def check_teaser_options(doc, teaser_option_name):
  # print(etree.tostring(doc))
  r = doc.xpath(
    "/atom:entry" +
    "/atom:content" +
    "/vdf:payload" +
    "/vdf:field[@name='page']" +
    "/vdf:value" +
    "/group:group" +
    "/group:area[@name='main']" +
    "/group:group" +
    "/vdf:payload" +
    "/vdf:field[@name='" + teaser_option_name + "']" +
    "/vdf:value",
    namespaces=ece.xml_namespaces)

  assert len(r) > 0
  for el in r:
    assert el.text in ["s", "m", "l"]


def check(conf):
  publication = conf["publication"]
  user = conf["user"]
  password = conf["password"]
  ws_base_url = conf["ws_base_url"]

  ece.create_publication(publication)
  section_page_id = ece.create_section_page(publication, user, password)

  url = ws_base_url \
      + "/escenic/section-page/" + str(section_page_id)
  auth = (user, password)
  response = requests.get(url, auth=auth)

  doc = etree.parse(StringIO(response.text))
  check_teaser_options(doc, "main-area-items-option-size")
  check_changing_teaser_options(url, auth, doc, "main-area-items-option-size")
