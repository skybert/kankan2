import requests
from lxml import etree
from lib import ece
from io import StringIO


def check_simple_array(doc, array_name):
  r = doc.xpath(
    '/vdf:model' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]' +
    '/vdf:listdef' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]',
    namespaces=ece.xml_namespaces)

  assert len(r) > 0


def check_complex_array_single_field(doc, array_name, field_name):
  r = doc.xpath(
    '/vdf:model' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]' +
    '/vdf:listdef' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]' +
    '/vdf:fielddef[@name="' + field_name + '"]',
    namespaces=ece.xml_namespaces)

  assert len(r) == 1
  assert r[0].get("name") == field_name


def check_complex_array_multi_field(doc, array_name, field_names):
  r = doc.xpath(
    '/vdf:model' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]' +
    '/vdf:listdef' +
    "/vdf:schema" +
    '/vdf:fielddef[@name="' + array_name + '"]' +
    '/vdf:fielddef',
    namespaces=ece.xml_namespaces)

  assert len(r) == 2
  assert r[0].get("name") == field_names[0]
  assert r[1].get("name") == field_names[1]


def check(ws_base_url, publication, content_type, user, password):
  ece.create_publication(publication)
  url = ws_base_url \
      + "/escenic/publication/" + publication \
      + "/model/content-type/" + content_type
  response = requests.get(url, auth=(user, password))
  xml = response.text
  f = StringIO(xml)
  doc = etree.parse(f)

  check_simple_array(doc, "simple-array")
  check_complex_array_single_field(
    doc,
    "single-item-complex-array",
    "f1-in-complex"
  )
  check_complex_array_multi_field(
    doc,
    "double-item-complex-array",
    ["f1-in-complex", "f2-in-complex"]
  )
