#!/usr/bin/env python2.7


import os,re,sys
import unittest

from Tools.test import *
from Tools.environments import *

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
