#!/usr/bin/python


import os,re,sys
import unittest

from _tools.test import *
from _tools.colours import *

class ColoursTest(unittest.TestCase):
    """Colours class test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_BlackAndWhite(self):
        """terminal colours with colour=False"""
        colours = Colours(colour=False)
        for colour in dir(colours):
            if not colour[0] == '_':
                sys.stdout.write(getattr(colours,colour))
                sys.stdout.write(colour)
                sys.stdout.write(colours.Off)
                print
        assert colours.Blue == ''
        return

    def dont_test_02_TerminalColours(self):
        """terminal colours with colour=True"""
        colours = Colours(colour=True)
        for colour in dir(colours):
            if not colour[0] == '_':
                sys.stdout.write(getattr(colours,colour))
                sys.stdout.write(colour)
                sys.stdout.write(colours.Off)
                print
        assert colours.Blue == '\033[34m'
        return

    def test_03_HTML_inColour(self):
        """terminal colours with colour=True and html=True"""
        colours = Colours(colour=True,html=True)
        for colour in dir(colours):
            if not colour[0] == '_':
                sys.stdout.write(getattr(colours,colour))
                sys.stdout.write(colour)
                sys.stdout.write(colours.Off)
                print
        assert colours.Blue == '<font color="Blue">'
        return


if __name__ == '__main__':
    unittest.main()
