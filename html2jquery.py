#!/usr/bin/env python

import os,re,sys,json,xmltodict

from Tools.argue import Argue

args = Argue()

@args.command(single=True)
class HtmlTojQuery(object):

    def process(self,item,output,indent=''):
        #print item, type(item)
        if not item:
            return
        if type(item) in [str,unicode]:
            output.write('%s.text("%s")\n'%(indent,item))
            return
        for key, value in item.iteritems():
            if key == '@class':
                output.write('%s.addClass("%s")\n'%(indent,value));
            elif key.startswith('@'):
                output.write('%s.attr("%s","%s")\n'%(indent,key.lstrip('@'),value));
            elif key == '#text':
                output.write('%s.text("%s")\n'%(indent,value))
            else:
                if type(value) == list:
                    for child in value:
                        output.write('%s.append(\n'%indent)
                        output.write('%s$("<%s/>")\n'%(indent+'  ',key));
                        self.process(child,output,indent=indent+'  '+'  ')
                        output.write('%s)\n'%indent);
                else:
                    output.write('%s.append(\n'%indent)
                    output.write('%s$("<%s/>")\n'%(indent+'  ',key));
                    self.process(value,output,indent=indent+'  '+'  ')
                    output.write('%s)\n'%indent);
        if indent == '':
            output.write(';');
        return
    
    @args.operation
    def convert(self, input, output=None):
        '''
        convert xhtml into jQuery code gen
        
        :param  input: the file name of the xhtml file
        
        :param output: the jQuery output file
        :short output: o

        '''
        _output = sys.stdout
        if output:
            _output = open(output,'w')

        with open(input) as _input:
            xhtml = xmltodict.parse(_input)
            self.process(xhtml,_output)
        if output:
            _output.close()

        return

if __name__ == '__main__': args.execute()

