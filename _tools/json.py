#!/usr/bin/python

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
