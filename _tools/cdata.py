#!/usr/bin/python

tokens = {
    '&amp;lt;' : '%%%%lt%%%%',
    '&amp;gt;' : '%%%%gt%%%%',
    '&amp;amp;' : '%%%%amp%%%%',
    '&amp;quot;' : '%%%%quot%%%%',
    '&amp;apos;' : '%%%%apos%%%%',
    '&lt;' : '<',
    '&gt;' : '>',
    '&amp;' : '&',
    '&quot;' : '\"',
    '&apos;' : '\'',
    '&nbsp;' : ' ',
    '%%%%lt%%%%' : '&lt;',
    '%%%%gt%%%%' : '&gt;',
    '%%%%amp%%%%' : '%amp;',
    '%%%%quot%%%%' : '%quot;',
    '%%%%apos%%%%' : '%apos;',
}

def cdata2xml(input,output):
    for line in input.readlines():
        for key in tokens.keys():
            while key in line:
                line = line.replace(key,tokens[key])
        output.write(line)
        output.flush()
