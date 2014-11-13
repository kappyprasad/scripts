#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import os,sys,re
import getpass,hashlib

from _tools.secrets import *

class Passwords(object):

    sshKeyFile = ''
    contextDir = '%s/.password'%os.environ['HOME']

    @property
    def username(self):
        return self.username
    @property
    def password(self):
        return self.password

    @classmethod
    def __init__(self,environment,username,clear=False):

        sshKeyFile = '%s/.ssh/id_rsa'%environment
        
        self.username = username
        self.password = None

        md5 = hashlib.md5()
        if os.path.isfile(self.sshKeyFile):
            fp = open(self.sshKeyFile)
            md5.update(''.join(fp.readlines()))
            fp.close()
        else:
            md5.update('%s@%s'%(username,environment))
        
        key = md5.digest()[0:8]

        secret = Secret(key)

        if not os.path.isdir(self.contextDir):
            os.mkdir(self.contextDir)

        contextFile = '%s/%s.%s'%(self.contextDir,environment,username)

        if not clear and os.path.isfile(contextFile):
            fp=open(contextFile)
            self.password = secret.decrypt(''.join(fp.readlines()))
            fp.close()
        else:
            self.password = getpass.getpass('env>%s, user>%s, pass>'%(environment,username))
            fp=open(contextFile,'w')
            fp.write(secret.encrypt(self.password))
            fp.close()
            
        return

