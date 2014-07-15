# shared tools for the CGU project

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/__init__.py $
# $Id: __init__.py 11546 2014-06-04 06:05:55Z david.edson $

#https://gist.github.com/romuald/1104222

import __builtin__
if not hasattr(__builtin__.property, "setter"):
    class property(__builtin__.property):
        __metaclass__ = type
        
        def setter(self, method):
            return property(self.fget, method, self.fdel)
            
        def deleter(self, method):
            return property(self.fget, self.fset, method)
            
        @__builtin__.property
        def __doc__(self):
            """Doc seems not to be set correctly when subclassing"""
            return self.fget.__doc__