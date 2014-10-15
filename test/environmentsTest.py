#!/usr/bin/python

# $Date: 2014-04-07 15:00:55 +1000 (Mon, 07 Apr 2014) $
# $Revision: 9930 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/test/environmentsTest.py $
# $Id: environmentsTest.py 9930 2014-04-07 05:00:55Z david.edson $


import os,re,sys
import unittest

from _tools.test import *
from _tools.environments import *

class EnvironmentsTest(unittest.TestCase):
    """Environments class test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_SVN_setup(self):
        """check to ensure that the SVN_MIDDLEWARE environment var is set"""
        assert 'SVN_MIDDLEWARE' in os.environ.keys()
        print 'SVN_MIDDLEWARE=%s'%os.environ['SVN_MIDDLEWARE']

    def test_02_GetMap(self):
        """test the map is returned with environments"""
        environments = Environments()
        assert environments
        assert len(environments.map) > 0
        for env in sorted(environments.map.keys()):
            print env
        return
    
    def test_03_GetDev1PC(self):
        """test that Dev1PC is in the list"""
        environments = Environments()
        assert 'Dev1PC' in environments.map.keys()
        dev1 = environments.map['Dev1PC']
        for sym in sorted(dev1.keys()):
            print sym
        
    def test_03_GetDev1PC_NODE_HOME(self):
        """test that the node home is set for Dev1PC"""
        environments = Environments()
        dev1 = environments.map['Dev1PC']
        assert 'NODE_HOME' in dev1.keys()
        nodeHome = dev1['NODE_HOME']
        print 'NODE_HOME=%s'%nodeHome
        assert nodeHome == '/cgu/dev1/was/profiles/Dev1CguPCN1'

    def test_04_GetDev1PC_APP_SVRS(self):
        """test that the app servers list is set for Dev1PC"""
        environments = Environments()
        dev1 = environments.map['Dev1PC']
        assert 'APP_SVRS' in dev1.keys()
        appSvrs = dev1['APP_SVRS']
        print 'APP_SVRS=%s'%appSvrs
        assert appSvrs == 'Dev1CguPCAppM1,Dev1CguPCAppM2'

if __name__ == '__main__':
    unittest.main()
