#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

class Fundamental(object):
    
    def __init__(self,xmi):
        self.xmi = xmi
        types = self.xmi.makePackage('Fundamental',self.xmi.modelNS)
        self.__types = {
            'String'   : self.xmi.makeClass('String',types),
            'Boolean'  : self.xmi.makeClass('Boolean',types),
            'Integer'  : self.xmi.makeClass('Integer',types),
            'Date'     : self.xmi.makeClass('Date',types),
            'Float'    : self.xmi.makeClass('Float',types),
        }
        return
