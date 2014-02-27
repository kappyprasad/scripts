#!/usr/bin/python

import xml.parsers.expat
from xml.dom import minidom
import sys, re

tokens = [
    { 
        'from' : '&amp;', 
        'into' : '####amp####' 
    },
    {
        'from' : '&',
        'into' : '&amp;'
    },
    {
        'from' : '<',
        'into' : '&lt;'
    },
    {
        'from' : '>',
        'into' : '&gt;'
    },
    {
        'from' : '\"',
        'into' : '&quot;'
    },
    {
        'from' : '\'',
        'into' : '&apos;'
    },
    {
        'from' : '####amp####',
        'into' : '&amp;'
    },
]

def escapeData(data):
    for token in tokens:
        data = data.replace(token['from'],token['into'])
    return data

class MyParser:
    indent = 0

    stateStartLast = 1
    stateEndLast = 2
    stateTextLast = 3
    stateCDataLast = 4
    stateCDataStart = 5
    stateCDataEnd = 6

    state = stateEndLast

    def __init__(self, colour=False, areturn=False, rformat=False, html=False, output=sys.stdout, preserve=False):

        self.output = output
        self.lt='<'
        self.gt='>'
        self.amp='&'
        self.quot='\"'
        self.apos='\''
        self.lf='\n'
        self.indentChar = '    '
        self.preserve = preserve
        
        if html:
            self.colOrange = '<font color="Orange">'
            self.colGreen = '<font color="Green">'
            self.colBlue = '<font color="Blue">'
            self.colTeal = '<font color="Teal">'
            self.colPurple = '<font color="Purple">'
            self.colRed = '<font color="Red">'
            self.colOff = '</font>'
            self.lt='&lt;'
            self.gt='&gt;'
            self.amp='&amp;'
            self.quot='&quot;'
            self.apos='&apos;'
            self.lf='<br/>'
            self.indentChar = '&nbsp;&nbsp;&nbsp;&nbsp;'
        elif colour:
            self.colOrange = '\033[33m'
            self.colGreen = '\033[32m'
            self.colBlue = '\033[34m'
            self.colTeal = '\033[36m'
            self.colPurple = '\033[35m'
            self.colRed = '\033[31m'
            self.colOff = '\033[0m'
        else:
            self.colOrange = ''
            self.colGreen = ''
            self.colBlue = ''
            self.colTeal = ''
            self.colPurple = ''
            self.colRed = ''
            self.colOff = ''

        self.areturn = areturn
        self.rformat = rformat
        
        self.parser = xml.parsers.expat.ParserCreate()

        self.parser.StartElementHandler          = self.startElementHandler
        self.parser.EndElementHandler            = self.endElementHandler
        self.parser.CharacterDataHandler         = self.characterDataHandler
        self.parser.CommentHandler               = self.commentHandler
        self.parser.StartCdataSectionHandler     = self.startCdataSectionHandler
        self.parser.EndCdataSectionHandler       = self.endCdataSectionHandler
        self.parser.XmlDeclHandler               = self.xmlDeclHandler
        self.parser.StartDoctypeDeclHandler      = self.startDoctypeDeclHandler
        self.parser.EndDoctypeDeclHandler        = self.endDoctypeDeclHandler
        self.parser.ProcessingInstructionHandler = self.processingInstructionHandler

        #         Doctype => \&handle_doctype,
        #         Proc => => \&handle_proc,

        self.leader = re.compile('(^\s+)')
        self.pattern = re.compile('(^\s+|\s+$)')
        self.lfCount = 0

        return

##parser.ElementDeclHandler(name, model)
##parser.AttlistDeclHandler(elname, attname, type, default, required)
##parser.UnparsedEntityDeclHandler(entityName, base, systemId, publicId, notationName)
##parser.EntityDeclHandler(entityName, is_parameter_entity, value, base, systemId, publicId, notationName)
##parser.NotationDeclHandler(notationName, base, systemId, publicId)
##parser.StartNamespaceDeclHandler(prefix, uri)
##parser.EndNamespaceDeclHandler(prefix)
##parser.DefaultHandler(data)
##parser.DefaultHandlerExpand(data)
##parser.NotStandaloneHandler()
##parser.ExternalEntityRefHandler(context, base, systemId, publicId)

    def close(self):
        if self.parser:
            self.parser.Parse('',1)
            del self.parser
        return
        
    def startElementHandler(self, name, attrs):
        if self.rformat:
            self.areturn = True

        if self.state == self.stateStartLast:
            self.output.write(
                self.colTeal + self.gt + self.colOff + self.lf
            )

        if self.preserve and self.lfCount > 2 and self.state == self.stateEndLast:
            self.output.write(self.lf)
            #self.output.write(',%s'%self.state)
        self.lfCount =0

        self.output.write((self.indent) * self.indentChar)
        self.output.write(
            self.colTeal + self.lt + self.colOff +
            self.colPurple + name + self.colOff
        )
        for attr in sorted(attrs.keys()):
            if self.areturn:
                self.output.write(self.lf)
                self.output.write((self.indent+1) * self.indentChar)
            else:
                self.output.write(' ')
            self.output.write(
                self.colRed + attr + self.colOff +
                self.colTeal + '=' + self.colOff + self.quot +
                self.colGreen + escapeData(attrs[attr]) + self.colOff + self.quot
            )
        if len(attrs) > 0 and self.areturn:
            self.output.write(self.lf)
            self.output.write((self.indent) * self.indentChar)
        self.indent += 1
        self.state = self.stateStartLast
        if self.rformat:
            self.rformat = False
            self.areturn = False
        return
            
    def endElementHandler(self, name):
        self.indent -= 1
        if self.state == self.stateCDataEnd:
            if self.lfCount > 1:
                self.output.write(self.lf)
                self.lfCount = 0
                
        if self.state == self.stateStartLast:
            self.output.write(
                self.colTeal + '/' + self.gt + self.colOff + self.lf
            )
        elif self.state != self.stateTextLast and self.state != self.stateCDataEnd:
            self.output.write((self.indent) * self.indentChar)
            self.output.write(
                self.colTeal + self.lt + self.colOff +
                self.colPurple + '/' + name + self.colOff +
                self.colTeal + self.gt + self.colOff + self.lf
            )
        else:
            self.output.write(
                self.colTeal + self.lt + self.colOff +
                self.colPurple + '/' + name + self.colOff +
                self.colTeal + self.gt + self.colOff + self.lf
            )
        self.state = self.stateEndLast
        return
        
    def characterDataHandler(self, data):
        if not self.state == self.stateCDataStart and not self.state == self.stateCDataLast:
            data = escapeData(data)

        leader = ''
        match = self.leader.match(data)
        if match:
            leader = match.group(1)

        self.lfCount = self.lfCount + data.count('\n')
        if not self.state == self.stateTextLast and not self.state == self.stateCDataLast:
            data = self.leader.sub('', data)
        if len(data) == 0:
            return

        if self.state == self.stateStartLast:
            self.output.write(self.colTeal + self.gt + self.colOff)
            if self.lfCount > 1:
                self.output.write(leader)
                self.output.write(self.lf)
            self.output.write(data)
            self.state = self.stateTextLast
        elif self.state == self.stateCDataStart:
            if self.lfCount > 0:
                self.output.write(leader)
                self.output.write(self.lf)
            self.output.write(data)
            self.state = self.stateCDataLast
        elif self.state == self.stateCDataLast:
            self.output.write(data)
        elif self.state == self.stateTextLast:
            self.output.write(data)
        elif self.state != self.stateEndLast:
            self.output.write(data)

        return
    
    def commentHandler(self, data):
        if self.state == self.stateStartLast:
            self.output.write(
                self.colTeal + self.gt + self.colOff + self.lf
            )
        self.output.write((self.indent) * self.indentChar)
        self.output.write(
            self.colTeal + self.lt + '!--' + data + '--' + self.gt + self.colOff + self.lf
        )
        self.state = self.stateEndLast
        return
        
    def startCdataSectionHandler(self):
        if not self.state == self.stateStartLast:
            self.output.write((self.indent) * self.indentChar)
        if self.state == self.stateStartLast:
            self.output.write(
                self.colTeal + self.gt + self.colOff
            )
        self.output.write(
            self.colTeal + self.lt + '![CDATA[' + self.colOff
        )
        self.state = self.stateCDataStart
        return
    
    def endCdataSectionHandler(self):
        self.output.write(
            self.colTeal + ']]' + self.gt + self.colOff
        )
        self.state = self.stateCDataEnd
        return
    
    def xmlDeclHandler(self, version, encoding, standalone):
        self.output.write((self.indent) * self.indentChar)
        self.output.write(
            self.colTeal + self.lt + '?xml ' + self.colOff +
            self.colRed + 'version' + self.colOff +
            self.colTeal + '=' + self.quot + self.colOff +
            self.colGreen + version + self.colOff +
            self.colTeal + self.quot + self.colOff
        )
        if encoding:
            self.output.write(' ' + 
                self.colRed + 'encoding' + self.colOff +
                self.colTeal + '=' + self.colOff + self.quot +
                self.colGreen + encoding + self.colOff + self.quot
            )
        self.output.write(
            self.colTeal + '?' +self.gt + self.colOff + self.lf
        )
        return
        
    def startDoctypeDeclHandler(self, doctypeName, systemId, publicId, has_internal_subset):
        self.output.write((self.indent) * self.indentChar)
        if not publicId:
            self.output.write(
                self.colTeal + self.lt + '!DOCTYPE ' + self.colOff +
                self.colOrange + doctypeName + self.colOff +
                self.colTeal + ' SYSTEM ' + self.quot + self.colOff +
                self.colGreen + systemId + self.colOff +
                self.colTeal + self.quot + self.quot + self.gt + self.colOff + self.lf
            )
        else:
            self.output.write(
                self.colTeal + self.lt + '!DOCTYPE ' + self.colOff +
                self.colOrange + doctypeName + self.colOff +
                self.colTeal + ' PUBLIC ' + self.quot + self.colOff + 
                self.colGreen + publicId + self.colOff + self.quot + ' ' + self.quot +
                self.colGreen + systemId + self.colOff +
                self.colTeal + self.quot+ self.gt + self.colOff + self.lf
            )
        return
        
    def endDoctypeDeclHandler(self):
        return
        
    def processingInstructionHandler(self, target, data):
        self.output.write((self.indent) * self.indentChar)
        self.output.write(
            self.colTeal + self.lt + '?' + target + self.colOff
        )
        pn = re.compile('\s*(\S+)=[\'"]([^\'"]*)[\'"]\s*')
        b = pn.split(data)
        while '' in b: b.remove('')
        for i in range(len(b)/2):
            self.output.write(' ' +
                self.colRed + b[2*i] + self.colOff + 
                self.colTeal + '=' + self.colOff + self.quot +
                self.colGreen + b[2*i+1] + self.colOff + self.quot
            )
        self.output.write(
            self.colTeal + '?' + self.gt + self.colOff + self.lf
        )
        return

