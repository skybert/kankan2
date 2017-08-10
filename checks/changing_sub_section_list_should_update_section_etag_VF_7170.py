import requests
from lxml import etree
from lib import ece
from io import StringIO
import uuid


def add_sub_section(section_uri, sub_section_uri, model_uri, auth):
  section_name = uuid.uuid4()

  xml = """
<entry
  xmlns="http://www.w3.org/2005/Atom"
  xmlns:metadata="http://xmlns.escenic.com/2010/atom-metadata">

  <title type="text">""" + str(section_name) + """</title>
  <link
    rel="http://www.vizrt.com/types/relation/parent"
    href='""" + section_uri + """' title="poetry"
    type="application/atom+xml; type=entry">
  </link>
  <content type="application/vnd.vizrt.payload+xml">
    <vdf:payload
        xmlns:vdf="http://www.vizrt.com/types"
        model='""" + model_uri + """'>
      <vdf:field name="com.escenic.sectionName">
        <vdf:value>""" + str(section_name) + """</vdf:value>
      </vdf:field>
    </vdf:payload>
  </content>
</entry>
  """

  headers = {
    "Content-type": "application/atom+xml"
  }
  response = requests.post(
    sub_section_uri,
    auth=auth,
    headers=headers,
    data=xml
  )

  assert response.status_code == 201


def check(conf):
  publication = conf["publication"]
  user = conf["user"]
  password = conf["password"]
  ws_base_url = conf["ws_base_url"]

  ece.create_publication(publication)
  section_id = ece.create_section(publication, user, password)
  section_uri = ws_base_url + "/escenic/section/" + str(section_id)
  auth = (user, password)
  response = requests.get(section_uri, auth=auth)
  etag_before = response.headers["ETag"]

  doc = etree.parse(StringIO(response.text))
  r = doc.xpath(
    "/atom:entry" +
    "/atom:link[@rel='down']",
    namespaces=ece.xml_namespaces)
  assert len(r) == 1
  assert r[0].get("href") is not ""
  sub_section_uri = r[0].get("href")

  model_uri = ws_base_url + \
      "/escenic/publication/" + publication + \
      "/model/content-type/com.escenic.section"

  add_sub_section(section_uri, sub_section_uri, model_uri, auth)
  response = requests.get(section_uri, auth=auth)
  assert response.status_code == 200
  assert "ETag" in response.headers

  etag_after_adding_section = response.headers["ETag"]
  assert etag_before != etag_after_adding_section
