#!/usr/bin/python





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

@XmlAccessorType(XmlAccessType.NONE)
@XmlType
@XmlRootElement
"""

classes = [
    'Entity',
    'Embeddable',
    'Transient',
    'GeneratedValue',
    'Temporal',
    'Lob',
    'OneToMany',
    'Column',
    'OneToOne',
    'MappedSuperclass',
    'ManyToOne',
    'Id',
]

classPatternStr = '^@(%s)\w.*'%('|'.join(classes))
classPattern = re.compile(classPatternStr)
print classPatternStr

def main():
    for f in findFiles(path='src/au/com/cgu/utils/logging/model',fileOrDir=True,pn='^.*.java$'):
        print f
        b = '%s.bak'%f
        os.rename(f,b)
        ip = open(b)
        op = open(f,'w')
        for line in ip.readlines():
            if classPattern.match(line):
                op.write('//%s'%line)
            else:
                op.write(line)
        op.close()
        ip.close()
    return

#if __name__ == '__main__' : main()
