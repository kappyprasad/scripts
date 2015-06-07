#!/usr/bin/env python2.7

import os,sys,re,json,argparse,xmltodict,struct

from subprocess import Popen, PIPE
from zipfile import ZipFile

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-d','--dump',    action='store_true', help='dump js')
parser.add_argument('docx',           action='store',      help='the MS word docx files', nargs='*')

args = parser.parse_args()

if args.verbose:
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

def readlnk(path):
    # http://stackoverflow.com/questions/397125/reading-the-target-of-a-lnk-file-in-python
    target = ''
    try:
        with open(path, 'rb') as stream:
            content = stream.read()
            # skip first 20 bytes (HeaderSize and LinkCLSID)
            # read the LinkFlags structure (4 bytes)
            lflags = struct.unpack('I', content[0x14:0x18])[0]
            position = 0x18
            # if the HasLinkTargetIDList bit is set then skip the stored IDList 
            # structure and header
            if (lflags & 0x01) == 1:
                position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
            last_pos = position
            position += 0x04
            # get how long the file information is (LinkInfoSize)
            length = struct.unpack('I', content[last_pos:position])[0]
            # skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
            position += 0x0C
            # go to the LocalBasePath position
            lbpos = struct.unpack('I', content[position:position+0x04])[0]
            position = last_pos + lbpos
            # read the string at the given position of the determined length
            size= (length + last_pos) - position - 0x02
            temp = struct.unpack('c' * size, content[position:position+size])
            target = ''.join([chr(ord(a)) for a in temp])
    except:
        # could not read the file
        pass
    return target

def cygpath(dospath):
    process = Popen('cygpath -au %s'%dospath,shell=True, stdout=PIPE)
    path = process.stdout.readline().rstrip('\n')
    del process
    return path


def main():
    for path in args.docx:
        if path.endswith('.lnk'):
            docx = readlnk(path)
        else:
            docx = path
        if not docx.endswith('.docx'):
            continue
        sys.stderr.write('%s\n'%docx)
        zip = ZipFile(docx)
        if args.verbose:
            for name in zip.namelist():
                sys.stderr.write('\t%s\n'%name)
        xml = zip.open('word/document.xml')
        js = xmltodict.parse(xml)
        if args.verbose:
            json.dump(js,sys.stderr,indent=4)
        if args.dump:
            output = open('%s.js'%path,'w')
            json.dump(js,output,indent=4)
            output.close()
        del xml
        del zip
    return

if __name__ == '__main__': main()




