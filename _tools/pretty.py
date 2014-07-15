#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/pretty.py $
# $Id: pretty.py 11546 2014-06-04 06:05:55Z david.edson $


import sys,os,re
from _tools.colours import *
import StringIO

########################################################################################################################
class PrettyObject(object):

    def __init__(self):
        None

########################################################################################################################
class PrettyPrinter(object):
    
    def __init__(self, output=sys.stdout, colour=True, html=False,align=False):
        self.output = output
        self.align = align
        self.colours = Colours(colour=colour, html=html)
        self.walked = []

    def prettify(self, d, indent=''):
        t='%s'%type(d)
        if d is None:
            self.output.write(self.colours.Off)
            self.output.write('None')
            self.output.write(self.colours.Off)
            
        elif isinstance(d,PrettyObject):
            name = '%s'%d.__class__.__name__
            if d in self.walked:
                self.output.write(self.colours.Purple)
                self.output.write('<%s hash="%d"/>'%(name,hash(d)))
                self.output.write(self.colours.Off)
                return
                
            self.walked.append(d)
            self.output.write(self.colours.Purple)
            self.output.write('<%s hash="%d">\n'%(name,hash(d)))
            self.output.write(self.colours.Off)
            
            keys = dir(d)
            for i in range(len(keys)):
                key = keys[i]
                if key[0] == '_':
                    continue
                    
                self.output.write('%s  '%indent)
                self.output.write(self.colours.Red)
                self.output.write('<%s>'%key)
                self.output.write(self.colours.Off)

                o = getattr(d,key)
                if isinstance(o,PrettyObject):
                    self.output.write('\n%s    '%indent)
                    self.prettify(o, indent='%s    '%indent)
                    self.output.write('\n%s  '%indent)
                else:
                    self.prettify(o, indent='%s  '%indent)
            
                self.output.write(self.colours.Red)
                self.output.write('</%s>'%key)
                self.output.write(self.colours.Off)
                self.output.write('\n')
                    
            self.output.write('%s'%indent)
            self.output.write(self.colours.Purple)
            self.output.write('</%s>'%name)
            self.output.write(self.colours.Off)
            
        elif t == 'org.python.core.PyDictionary' or t == '<type \'dict\'>':
            self.output.write(self.colours.Purple)
            self.output.write('{')
            self.output.write(self.colours.Off)
            self.output.write('\n')

            width = max(map(lambda x : len(x), d.keys()))

            keys = d.keys()
            for i in range(len(keys)):
                key = keys[i]

                if self.align:
                    padding = width-len(key)
                else:
                    padding = 0
                    
                self.output.write('%s  \''%indent)
                self.output.write(self.colours.Red)
                self.output.write('%s'%key)
                self.output.write(self.colours.Off)
                self.output.write('\'%s :  '%(' '*padding))
                
                self.prettify(d[key], indent='%s  '%indent)
                
                if i < (len(keys) - 1):
                    self.output.write(',\n')
                else:
                    self.output.write('\n')
                    
            self.output.write('%s'%indent)
            self.output.write(self.colours.Purple)
            self.output.write('}')
            self.output.write(self.colours.Off)
            
        elif t == 'org.python.core.PyList' or t == '<type \'list\'>':
            if len(self.walked) == 0:
                self.bracket(d,'[',']','Teal','  %s'%indent)
            else:
                self.bracket(d,'','','Teal','  %s'%indent)
                        
        elif t == 'org.python.core.PyTuple' or t == '<type \'tuple\'>':
            if len(self.walked) == 0:
                self.bracket(d,'(',')','Orange','  %s'%indent)
            else:
                self.bracket(d,'','','Orange','  %s'%indent)
                
        elif t == 'org.python.core.PyString' or t == '<type \'str\'>':
            if len(self.walked) == 0:
                self.output.write('\'')
            self.output.write(self.colours.Green)
            self.output.write('%s'%d)
            self.output.write(self.colours.Off)
            if len(self.walked) == 0:
                self.output.write('\'')

        else:
            self.output.write(self.colours.Green)
            self.output.write('%s'%d)
            self.output.write(self.colours.Off)

        if len(indent) == 0:
            self.output.write('\n')
            
        return
    
    def bracket(self, d, start, end, colour, indent):
        self.output.write(getattr(self.colours,colour))
        self.output.write('%s\n' % start)
        self.output.write(self.colours.Off)
        
        for i in range(len(d)):
            self.output.write('%s' % (indent))
            self.prettify(d[i], indent='%s' % indent)
            if len(self.walked) == 0 and i < (len(d) - 1):
                self.output.write(',\n')
            else:
                self.output.write('\n')
                
        self.output.write('%s'%indent[:-2])
        self.output.write(getattr(self.colours,colour))
        self.output.write('%s'%end)
        self.output.write(self.colours.Off)
        
        return


########################################################################################################################
class TestPrettyObject(PrettyObject):

    def __init__(self,name=''):
        self.name = name    
        self.partner = None
        self.children = []
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,value):
        self.__name = value
        
    @name.deleter
    def name(self):
        del self.__name

    @property
    def partner(self):
        return self.__partner
    
    @partner.setter
    def partner(self,value):
        self.__partner = value
        
    @partner.deleter
    def partner(self):
        del self.__partner
    
    @property
    def children(self):
        return self.__children
    
    @children.setter
    def children(self, value):
        self.__children = value
        
    @children.deleter
    def children(self):
        del self.__children

########################################################################################################################
def prettyPrint(object,output=sys.stdout,colour=True,align=True):
    printer = PrettyPrinter(output=output,colour=colour,align=align)
    printer.prettify(object)
    del printer
    return

########################################################################################################################
def main():
    
    json = '{ "hello" : "there", "you" : 0, "array" : [ "one",2,3.4 ], "tupple" : ( "a", 1, 2.3, 4.5),  "object" : { "true": True, "false" : False } }'
    print json
    print
    pyson = eval(json)
    print pyson
    
    so = StringIO.StringIO()
    printer = PrettyPrinter(output=so,colour=False)
    printer.prettify(pyson)
    prettyJson = so.getvalue()
    print prettyJson
    
    del printer
    
    prettyPyson = eval(prettyJson)
    assert prettyPyson["object"]["false"] == False
    assert prettyPyson["array"][1] == 2
    
    print
    printer = PrettyPrinter(colour=True)
    printer.prettify(prettyPyson)
    del printer

    print
    dad = TestPrettyObject()
    dad.name = 'Dad'

    mum = TestPrettyObject(name='Mum')
    mum.partner = dad
    dad.partner = mum
    
    son = TestPrettyObject(name='Son')
    sis = TestPrettyObject(name='Sis')

    dad.children = [son]    
    dad.children.append(sis)
    
    mum.children.append(son)
    mum.children.append(sis)

    printer = PrettyPrinter(colour=True)
    printer.prettify(dad)
    del printer
    
    return

########################################################################################################################
if __name__ == '__main__': main()
