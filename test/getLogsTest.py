#!/usr/bin/python

# $Date: 2014-04-07 15:00:55 +1000 (Mon, 07 Apr 2014) $
# $Revision: 9930 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/test/getLogsTest.py $
# $Id: getLogsTest.py 9930 2014-04-07 05:00:55Z david.edson $

import os,re,sys
import unittest

from _tools.test import *
from _tools.environments import *

class GetLogsTest(unittest.TestCase):
    """getLogs script test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_GetMap(self):
        """test the map is returned with environments"""
        environments = Environments()
        assert environments
        assert len(environments.map) > 0
        for env in sorted(environments.map.keys()):
            print env
        return

    def test_02_GetDev1PS(self):
        """test that Dev1PS is in the list"""
        environments = Environments()
        assert 'Dev1PS' in environments.map.keys()
        dev1 = environments.map['Dev1PS']
        for sym in sorted(dev1.keys()):
            print sym    

if __name__ == '__main__':
    unittest.main()
