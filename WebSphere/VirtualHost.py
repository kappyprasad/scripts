#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class VirtualHost(WebSphere.Entity):

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self,host):
        self.__host = host
        return

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self,port):
        self.__port = port
        return

    def __init__(self):
        super(VirtualHost, self).__init__()
        self.__host = None
        self.__port = 0
        return
