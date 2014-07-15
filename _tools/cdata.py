#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


xml2cdataTokens = {
    '&amp;lt;'     : '%%%%lt%%%%',
    '&amp;gt;'     : '%%%%gt%%%%',
    '&amp;amp;'    : '%%%%amp%%%%',
    '&amp;quot;'   : '%%%%quot%%%%',
    '&amp;apos;'   : '%%%%apos%%%%',
    '&lt;'         : '<',
    '&gt;'         : '>',
    '&amp;'        : '&',
    '&quot;'       : '\"',
    '&apos;'       : '\'',
    '&nbsp;'       : ' ',
    '%%%%lt%%%%'   : '&lt;',
    '%%%%gt%%%%'   : '&gt;',
    '%%%%amp%%%%'  : '%amp;',
    '%%%%quot%%%%' : '%quot;',
    '%%%%apos%%%%' : '%apos;',
}

cdata2xmlTokens = {
    '&'            : '%%%%amp%%%%',
    '<'            : '&lt;',
    '>'            : '&gt;',
    '\"'           : '&quot;',
    '\''           : '&apos;',
    '%%%%amp%%%%'  : '&amp;',
}

def cdata2xml(input,output):
    for line in input.readlines():
        output.write(cdata2xmlTokenize(line))
        output.flush()

def cdata2xmlTokenize(line):
    for key in cdata2xmlTokens.keys():
        while key in line:
            line = line.replace(key,cdata2xmlTokens[key])
    return line

def xml2cdata(input,output):
    for line in input.readlines():
        output.write(xml2cdataTokenize(line))
        output.flush()

def xml2cdataTokenize(line):
    for key in xml2cdataTokens.keys():
        while key in line:
            line = line.replace(key,xml2cdataTokens[key])
    return line
