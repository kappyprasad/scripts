#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/secrets.py $
# $Id: secrets.py 11546 2014-06-04 06:05:55Z david.edson $

import os,re,sys

from Crypto.Cipher import DES

class Secret:

    @classmethod
    def __init__(self,key):
        key = key
        while len(key) % 8 != 0:
            key += '_'
        self.des = DES.new(key,DES.MODE_ECB)

    @classmethod
    def encrypt(self,value):
        padding = ''
        while len(value) % 8 != 0:
            padding += '_'
            value = value + padding
        encrypted = self.des.encrypt(value)
        return '%s,%s'%(padding,encrypted)

    @classmethod
    def decrypt(self,value):
        p = re.compile('^(_*),(.*)$')
        (padding,encrypted) = p.match(value).groups()
        decrypted = self.des.decrypt(encrypted)
        return decrypted.rstrip(padding)
        
