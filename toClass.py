#!/usr/bin/python

import os,sys,re,json,argparse

parser = argparse.ArgumentParser('make a python script into a class')

parser.add_argument('-v', '--verbose', action='store_true',                    help='show verbose output')
parser.add_argument('-i', '--inplace', action='store_true',                    help='replace existing file')
parser.add_argument('-o', '--output',  action='store',                         help='output to file')
parser.add_argument('-t', '--tab',     action='store',     default='    ',     help='indent characters')
parser.add_argument('-c', '--clasz',   action='store',     required=True,      help='the name of the class required')
parser.add_argument('-a', '--attr',    action='store',     default='@',        help='attribute prefix to harvest attributes')
parser.add_argument('-b', '--body',    action='store',     default='^',        help='method prefix fo harvest methods')
parser.add_argument('-m', '--main',    action='store',     default=':',        help='main prefix to harvest main __init__()')
parser.add_argument('-l', '--last',    action='store',     default='$',        help='last prefix insert main() call')
parser.add_argument('file',            action='store',     nargs='*',          help='the file name')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args:')
    json.dump(vars(args),sys.stderr,indent=4)


################################################################################
class State(object):

    _instance = None

    classPattern  = re.compile('^\\%s.*'%args.body)
    attrPattern   = re.compile('^\\%s.*'%args.attr)
    mainPattern   = re.compile('^\\%s.*'%args.main)
    lastPattern   = re.compile('^\\%s.*'%args.last)
     
    def __new__(cls,*args,**kwargs):
        ''' singleton pattern '''
        if not cls._instance:
            cls._instance = super(State,cls).__new__(cls,*args,**kwargs)
        return cls._instance

    def __init__(self):
        '''constructor'''

    def before(self,line,output):
        raise NotImplementedError()

    def process(self,line,output):
        raise NotImplementedError()

################################################################################
class BeforeClass(State):
    def before(self,line,output):
        return
    def process(self,line,output):
        if self.classPattern.match(line) or self.attrPattern.match(line):
            state = InClass()
            state.before(line,output)
            return state
        output.write('%s\n'%line)
        return self

################################################################################
class InClass(State):
    methodPattern = re.compile('^\\%sdef\s([^\(]+)\(([^\)]*)\)\:(.*)$'%args.body)
    def before(self,line,output):
        output.write('class %s(object):\n\n'%args.clasz)
        output.write('%s%s\n'%(args.tab,line.lstrip('[%s%s]'%(args.attr,args.body))))
        return
    def process(self,line,output):
        isMethod = self.methodPattern.match(line)
        if isMethod:
            (name,params,rest) = isMethod.groups()
            output.write('\n%sdef %s(self,%s):%s\n'%(args.tab,name,params,rest))
            return self
        if self.mainPattern.match(line):
            state = InMain()
            state.before(line,output)
            return state
        if self.classPattern.match(line):
            output.write('%s%s\n'%(args.tab,line.lstrip('^')))
            return self
        if self.lastPattern.match(line):
            state = AfterAll()
            state.before(line,output)
            return state
        return self

################################################################################
class InMain(State):
    def before(self,line,output):
        output.write('\n%sdef __init__(self):\n'%args.tab)
        output.write('%s%s\n'%(args.tab*2,line.lstrip(args.main)))
        return
    def process(self,line,output):
        if self.lastPattern.match(line):
            state = AfterAll()
            state.before(line,output)
            return state
        output.write('%s%s\n'%(args.tab*2,line.lstrip(args.main)))
        return self

################################################################################
class AfterAll(State):
    def before(self,line,output):
        output.write('\ndef main():\n%sinstance=%s()\n'%(args.tab,args.clasz))
        output.write('\nif __name__ == \'__main__\': main()\n')
        return
    def process(self,line,output):
        output.write('%s\n'%line)
        return self

################################################################################
def process(input,output):
    state = BeforeClass()
    while True:
        line = input.readline()
        if not line:
            break
        line = line.rstrip('\n').rstrip('\r')
        state = state.process(line,output)
    return

def main():
    for file in args.file:
        if args.inplace:
            backup='%s.bak'
            if os.path.isfile(backup):
                os.unlink(backup)
            os.rename(file,backup)
            sys.stderr.write('%s\n'%file)
            input=open(backup)
            output=open(file,'w')
            process(input,output)
            output.close()
            input.close()
        else:
            input=open(file)
            output=sys.stdout
            process(input,output)
    return

if __name__ == '__main__': main()
