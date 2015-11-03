#!/usr/bin/env python2.7

import sys, re, os

from Tools.xpath import *
from Tools.parser import *
from Tools.eddo import *
from Tools.finder import *

xmldefinition="""
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.XmlType;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType
@XmlRootElement
"""

package="""
@javax.xml.bind.annotation.XmlSchema(
    namespace = "ns://%s",
    elementFormDefault = javax.xml.bind.annotation.XmlNsForm.QUALIFIED
)

package %s;
"""

classes = [
    '@Entity',
    '@Embeddable',
    '@javax.persistence.Entity',
    '@javax.persistence.Embeddable',
    '@MappedSuperclass',
    '@javax.persistence.MappedSuperclass',
]

attributes = [
    'String',
    'long',
    'int',
    'BigDecimal',
    'Date',
    'String',
    'double',
]

packagePatternStr = '^package (\S+);'
packagePattern = re.compile(packagePatternStr)

classPatternStr = '^(%s).*'%'|'.join(classes)
classPattern = re.compile(classPatternStr)

attrPatternStr = '^\s+private\s(%s)\s.*'%'|'.join(attributes)
attrPattern = re.compile(attrPatternStr)

def main():
    for f in findFiles(path='.',fileOrDir=True,pn='^.*.java$'):
        hasXmlRoot = False
        hasXmlAttr = False

        
        print f
        b = '%s.bak'%f
        os.rename(f,b)
        ip = open(b)
        op = open(f,'w')
        for line in ip.readlines():

            pm = packagePattern.match(line)
            if pm:
                pkg = pm.group(1)
                dir = os.path.dirname(f)
                pij = '%s/package-info.java'%dir
                if not os.path.isfile(pij):
                    fo = open(pij,'w')
                    fo.write(package%(pkg,pkg))
                    fo.close()
                            
            if '@XmlRootElement' in line:
                hasXmlRoot = True
            if classPattern.match(line) and not hasXmlRoot:
                op.write(xmldefinition)
                hasXmlRoot = True

            line = line.replace('Timestamp','Date')
            line = line.replace('java.sql.Date','java.util.Date')

            if '@XmlAttribute' in line:
                hasXmlAttr = True
            if attrPattern.match(line) and not hasXmlAttr:
                op.write('    @XmlAttribute\n')
                hasXmlAttr = False

            op.write(line)
        op.close()
        ip.close()
    return

if __name__ == '__main__' : main()
