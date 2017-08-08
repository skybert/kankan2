import requests
from lxml import etree
from lib import ece
from io import StringIO


def check_changing_teaser_options(doc, teaser_option_name):
  pass


def check_teaser_options(doc, teaser_option_name):

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
    "/vdf:field[@name='" + teaser_option_name + "']",
    namespaces=ece.xml_namespaces)

  assert len(r) > 0


def check(conf):
  publication = conf["publication"]
  user = conf["user"]
  password = conf["password"]
  ws_base_url = conf["ws_base_url"]

  ece.create_publication(publication)
  section_page_id = ece.create_section_page(publication, user, password)

  url = ws_base_url \
      + "/escenic/section-page/" + str(section_page_id)

  response = requests.get(url, auth=(user, password))
  # print(response.text)

  xml = response.text
  f = StringIO(xml)
  doc = etree.parse(f)

  check_teaser_options(doc, "main-area-items-option-size")
