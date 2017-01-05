#!/usr/bin/env python

import lxml.etree as ET

xml_filename = sys.argv[1]
xsl_filename = ''
dom = ET.parse(xml_filename)
xslt = ET.parse(xsl_filename)
transform = ET.XSLT(xslt)
newdom = transform(dom)
print(ET.tostring(newdom, pretty_print=True))
