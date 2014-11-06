#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



import sys,os,re,StringIO
from _tools.colours import *

import Types

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
            
        elif \
             isinstance(d,Types.List) \
             or \
             isinstance(d,Types.Map) \
             or \
             isinstance(d,Types.Typed) \
             or \
             isinstance(d,Types.Object) \
             :
            name = '%s'%d.__class__.__name__
            #sys.stderr.write('name=%s\n'%name)

            if d in self.walked:
                self.output.write(self.colours.Purple)
                self.output.write('<%s hash="%d"/>'%(name,hash(d)))
                self.output.write(self.colours.Off)
                return
            self.walked.append(d)

            if isinstance(d,Types.Map) or isinstance(d,Types.List):
                self.output.write('%s%s'%(indent,self.colours.Green))
            else:
                self.output.write('%s%s'%(indent,self.colours.Purple))

            if isinstance(d,Types.Object):
                self.output.write('<%s hash="%d">\n'%(name,hash(d)))
            elif (isinstance(d,Types.List) or isinstance(d,Types.Map)) and len(d) == 0:
                self.output.write('<%s type="%s" hash="%d"/>'%(name,d.type,hash(d)))
                self.output.write(self.colours.Off)
                return
            else:
                self.output.write('<%s type="%s" hash="%d">\n'%(name,d.type,hash(d)))
                self.output.write(self.colours.Off)

            if isinstance(d,Types.List):
                keys = range(len(d))
            elif isinstance(d,Types.Map):
                keys = d.keys()
            else:
                keys = dir(d)

            for key in keys:
                #sys.stderr.write('key=%s\n'%key)

                if isinstance(d,Types.List):
                    o = d[key]
                elif isinstance(d,Types.Map):
                    o = d[key]
                else:
                    #if key[0] == '_': continue
                    o = getattr(d,key)

                #sys.stderr.write('value=%s'%o)

                if isinstance(d,Types.Map):
                    self.output.write(self.colours.Teal)
                    self.output.write('%s  <Item %s="%s">'%(indent,d.key,key))
                    self.output.write('%s\n'%(self.colours.Off))
                    self.prettify(o, indent='%s    '%indent)
                    self.output.write(self.colours.Teal)
                    self.output.write('\n%s  </Item>\n'%indent)
                    self.output.write(self.colours.Off)

                elif isinstance(d,Types.List):
                    if isinstance(o,Types.Object):
                        self.prettify(o, indent='%s  '%indent)
                    else:
                        sys.stdout.write('%s  <%s>%s</%s>'%(
                            indent,o.__class__.__name__,o,o.__class__.__name__
                        ))
                    self.output.write('\n')
                else:
                    self.output.write(self.colours.Orange)
                    self.output.write('%s  <%s>'%(indent,key))
                    self.output.write('%s'%(self.colours.Off))

                    if isinstance(o,Types.Map):
                        self.output.write('\n')
                        self.prettify(o, indent='%s    '%indent)
                        self.output.write('\n%s  '%indent)
                    elif isinstance(o,Types.Object):
                        self.output.write('\n')
                        self.prettify(o, indent='%s    '%indent)
                        self.output.write('\n%s  '%indent)
                    elif isinstance(o,Types.Typed):
                        if o.value != None:
                            self.output.write('%s'%o)
                    else:
                        self.output.write('%s'%o)

                    self.output.write(self.colours.Orange)
                    self.output.write('</%s>\n'%(key))
                    self.output.write(self.colours.Off)
                                    
            if isinstance(d,Types.Map) or isinstance(d,Types.List):
                self.output.write('%s%s'%(indent,self.colours.Green))
            else:
                self.output.write('%s'%indent)
                self.output.write(self.colours.Purple)

            self.output.write('</%s>'%name)
            self.output.write(self.colours.Off)
            
        elif t == 'org.python.core.PyDictionary' or t == '<type \'dict\'>':
            self.output.write(self.colours.Purple)
            self.output.write('{')
            self.output.write(self.colours.Off)
            self.output.write('\n')

            if len(d) > 0:
                width = max(map(lambda x : len(x), d.keys()))
            else:
                width = 0

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
class TestPrettyObject(Types.Object):

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
def prettyPrint(object,output=sys.stdout,colour=True,align=True,html=False):
    printer = PrettyPrinter(output=output,colour=colour,align=align,html=html)
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
