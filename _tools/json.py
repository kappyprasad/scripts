#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/json.py $
# $Id: json.py 11546 2014-06-04 06:05:55Z david.edson $

replacements = {
    ':false' : ':False',
    ':true'  : ':True',
    ':null'  : ':None',
    '[null'  : '[None',
    ',null'  : ',None',
}

def parseJSON(lines):
    for replacement in replacements.keys():
        while replacement in lines:
            lines = lines.replace(replacement,replacements[replacement])
    return eval(lines)
