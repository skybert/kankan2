
from io import StringIO
from lxml import etree


xml_namespaces = {
    "atom": "http://www.w3.org/2005/Atom",
    "ui": "http://xmlns.escenic.com/2008/interface-hints",
    "ct": "http://xmlns.escenic.com/2008/content-type",
    "vdf": "http://www.vizrt.com/types",
    "group": "http://xmlns.escenic.com/2015/layout-group",
    "thr": "http://purl.org/syndication/thread/1.0"
}


def create_publication(name):
  # TODO implement me
  pass


def create_section_page(publication, user, password):
  # TODO implement me
  if publication == "rohan":
    return 13612
  else:
    return 1


def create_section(publication, user, password):
  # TODO implement me
  if publication == "rohan":
    return 194
  else:
    return 1


def get_sub_section_uri(xml):
  doc = etree.parse(StringIO(xml))
  r = doc.xpath(
    "/atom:entry" +
    "/atom:link[@rel='down']",
    namespaces=xml_namespaces)
  assert len(r) == 1
  assert r[0].get("href") is not ""
  return r[0].get("href")
