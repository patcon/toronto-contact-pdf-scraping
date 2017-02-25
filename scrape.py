import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from lxml import etree

tree = etree.parse('sources/city_clerk_office.xml')
root = tree.getroot()

headers = []
headers.append(root.xpath("//fontspec[@family='Times' and @size='19' and @color='#ffffff']")[0])
headers.append(root.xpath("//fontspec[@family='Times' and @size='16' and @color='#000000']")[0])
headers.append(root.xpath("//fontspec[@family='Times' and @size='12' and @color='#000000']")[1])
for font in headers:
    print(font.attrib)
#elems = root.xpath(".//text[@font='9']")
#elems = root.xpath(".//text[@font='1']")
xpath_filter = ' or '.join(["@font='{}'".format(font.attrib['id']) for font in headers])
elems = root.xpath(".//text[{}]".format(xpath_filter))
#elems = root.xpath(".//text[" + attrib_selector + "]")
elems = iter(elems)
for e in elems:
    header = e.xpath('./b')[0].text
    if not header.strip():
        continue

    next_e = e.xpath('./following-sibling::text')[0]
    if next_e.attrib['font'] == e.attrib['font']:
        next_header = next_e.xpath('./b')[0].text
        header = header + next_header
        elems.__next__()
    print('"{}",{}'.format(header.strip(), e.attrib['font']))
