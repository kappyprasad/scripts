#!/usr/bin/python





import sys,StringIO

colours = {
	'Orange' : '\033[33m',
	'Green'  : '\033[32m',
	'Blue'   : '\033[34m',
	'Teal'   : '\033[36m',
	'Purple' : '\033[35m',
	'Red'    : '\033[31m',
	'Off'    : '\033[0m'
}

def convertStream(ip,op):
    for line in ip.readlines():
        op.write('<p>')
        for key in colours.keys():
            if key == 'Off':
                line = line.replace(colours[key],'</font>')
            else:
                line = line.replace(colours[key],'<font color="%s">'%key)
        op.write('%s\n'%line)
        op.write('</p>\n')
    return

def toHtml(coloured):
    ip = StringIO.StringIO(coloured)
    op = StringIO.StringIO()
    convertStream(ip,op)
    html = op.getvalue()
    op.close()
    return html

def main():
    convertStream(sys.stdin,sys.stdout)
    return

if __name__ == '__main__' : main()
