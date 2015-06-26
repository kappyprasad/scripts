#!/usr/bin/env python2.7

import sys, re, os

from Tools.finder import *

classPattern = re.compile('^.*$')
attrPattern  = re.compile('^(\s+private\s+(\S+)\s+([^\s;]+))(.*)$')
endPattern   = re.compile('^}')
listPattern  = re.compile('^List<([^>]+)>$')

def upName(name):
    upper = '%s%s'%(name[0].upper(),name[1:])
    return upper

def getter(name,type):
    upper = upName(name)
    method = """
    public %s get%s() {
        return %s;
    }
"""%(type,upper,name)
    return method

def setter(name,type):
    upper = upName(name)
    method = """
    public void set%s(%s %s) {
        this.%s = %s;
    }
"""%(upper,type,name,name,name)
    return method

def lister(name,type):
    upper = upName(name)
    method = """
    public %s get%s() {
        if (%s == null) {
            %s = new ArrayList<%s>();
        }
        return %s;
    }
"""%('List<%s>'%type,upper,name,name,type,name)
    return method

def main():
    for f in findFiles(path='.',fileOrDir=True,pn='^.*.java$'):

        attributes = {}

        sys.stderr.write('%s\n'%f)
        b = '%s.bak'%f
        os.rename(f,b)
        ip = open(b)
        op = open(f,'w')

        for line in ip.readlines():
            line = line.rstrip('\r')
            line = line.rstrip('\n')

            m = attrPattern.match(line)
            if m:
                attributes[m.group(3)] = m.group(2);
                op.write('%s;\n'%m.group(1))
                continue
                    
            if endPattern.match(line):
                op.write('// getters/setters\n')
                for attribute in attributes.keys():
                    type = attributes[attribute]
                    m = listPattern.match(type)
                    if m:
                        type = m.group(1)
                        op.write(lister(attribute,type))
                    else:
                        op.write(getter(attribute,type))
                        op.write(setter(attribute,type))

            op.write('%s\n'%line)

        op.close()
        ip.close()
    return

if __name__ == '__main__' : main()

