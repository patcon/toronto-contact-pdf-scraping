#!/usr/bin/env python
import subprocess
import sys
import xml.etree.ElementTree as ET

from xml.etree.ElementTree import tostring
from lxml import etree

try:
    xml_file = sys.argv[1]
except IndexError:
    print('Usage: {} <pdf file>'.format(sys.argv[0]))
    exit(0)

proc = subprocess.Popen(["pdftohtml", xml_file,  "-xml", "-i", "-stdout"], stdout=subprocess.PIPE)
out = proc.communicate()[0]

root = etree.fromstring(out)

headers = []
data = [x.split() for x in ['19 ffffff 0', '16 000000 1', '12 000000 1']]
for datum in data:
    size, color, i = datum
    i = int(i)
    q = "//fontspec[@family='Times' and @size='{}' and @color='#{}']".format(size, color)
    fontspec = root.xpath(q)
    headers += fontspec

debug = False
if debug:
    for font in headers:
        print(font.attrib)

xpath_filter = ' or '.join(["@font='{}'".format(font.attrib['id']) for font in headers])
elems = root.xpath(".//text[{}]".format(xpath_filter))
elems = iter(elems)
for e in elems:
    if not e.xpath('./b'):
        continue
    header = e.xpath('./b')[0].text.strip()
    if not header:
        continue

    next_e = e.xpath('./following-sibling::text')[0]
    if next_e.attrib['font'] == e.attrib['font']:
        if not next_e.xpath('./b'): continue
        next_header = next_e.xpath('./b')[0].text.strip()
        if next_header.startswith('Wards'): continue
        header = header + ' ' + next_header
        elems.__next__()
    print('"{}",{}'.format(header, e.attrib['font']))
