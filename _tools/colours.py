#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/colours.py $
# $Id: colours.py 11546 2014-06-04 06:05:55Z david.edson $

import sys,os,re

########################################################################################################################
colours = {
    'Orange': '\033[33m',
    'Green' : '\033[32m',
    'Blue'  : '\033[34m',
    'Teal'  : '\033[36m',
    'Purple': '\033[35m',
    'Red'   : '\033[31m',
    'Off'   : '\033[0m'
}

def getColours(html=False):
    if html:
        for key in colours.keys():
            if key != 'Off':
                colours[key] = '<font color="%s">'%key
            else:
                colours[key] = '</font>'
    return colours

########################################################################################################################
class Colours(object):

    def __init__(self, colour=True, html=False):
        self.__colours = {}
        self.__colour = colour
        self.__html = html

        if self.__colour:
            for key in colours.keys():
                self.__colours[key] = colours[key]
        else:
            for key in colours.keys():
                self.__colours[key] = ''

        try:
            import console
            for key in colours.keys():
                self.__colours[key] = ''
            self.console = True
        except:
            self.console = False
            
        if self.__html:
            for key in colours.keys():
                if key != 'Off':
                    self.__colours[key] = '<font color="%s">'%key
                else:
                    self.__colours[key] = '</font>'

    @property
    def Orange(self):
        if self.console:
            import console
            console.set_color(0.8,0.8,0)
        return self.__colours['Orange']

    @property
    def Green(self):
        if self.console:
            import console
            console.set_color(0,1,0)
        return self.__colours['Green']

    @property
    def Blue(self):
        if self.console:
            import console
            console.set_color(0,0,1)
        return self.__colours['Blue']

    @property
    def Teal(self):
        if self.console:
            import console
            console.set_color(0.5,0.5,1)
        return self.__colours['Teal']

    @property
    def Purple(self):
        if self.console:
            import console
            console.set_color(1,0,1)
        return self.__colours['Purple']

    @property
    def Red(self):
        if self.console:
            import console
            console.set_color(1,0,0)
        return self.__colours['Red']

    @property
    def Off(self):
        if self.console:
            import console
            console.set_color(0,0,0)
        return self.__colours['Off']

########################################################################################################################
def main():
    colours = Colours(colour=True)
    for colour in dir(colours):
        if not colour[0] == '_':
            sys.stdout.write(getattr(colours,colour))
            sys.stdout.write(colour)
            sys.stdout.write(colours.Off)
            print

    return

########################################################################################################################
if __name__ == '__main__': main()
