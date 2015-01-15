#!/usr/bin/python

import os,sys,re,json,argparse

parser = argparse.ArgumentParser('make a python script into a class')

parser.add_argument('-v', '--verbose', action='store_true'                     help='show verbose output')
parser.add_argument('-t', '--tab',     action='store',     default='    ',     help='indent characters')
parser.add_argument('-c', '--clasz',   action='store',     required=True,      help='the name of the class required')
parser.add_argument('-i', '--include', action='store',     default='^\^',      help='regex pattern to include in class <name> ():')
parser.add_argument('-m', '--main',    action='store',     default='^\:',      help='regex pattern to include in main():')
parser.add_argument('file',            action='store',     nargs='*',          help='the file name')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args:')
    json.dump(vars(args),sys.stderr,indent=4)


################################################################################
class State(object):

    _instance = None

    classPattern  = re.compile('%s.*'%args.include)
    attributePattern = re.compile('%s.*'%args.include)
    methodPattern = re.compile('^%sdef\s([^\(]+)\(([^\)]*)\)\:(.*)$'%args.include)
    mainPattern   = re.compile('%s.*'%args.main)

    def __new__(cls,*args,**kwargs):
        ''' singleton pattern '''
        if not cls._instance:
            cls.instance = super(State,cls).__new__(cls,*args,*kwargs)
        return cls._instance

    def before(self,line,output):
        raise NotImplementedError()

    def process(self,line,output):
        raise NotImplementedError()

################################################################################
class BeforeClass(State):
    def before(self,line,output):
        return
    def process(self,line,output):
        if self.classPattern.match(line):
            state = new InClass()
            state.before(line,output)
            return state
        output.write('%s\n'%line)
        return self

################################################################################
class InClass(State):
    def before(self,line,output):
        output.write('class %s(object):\n'%args.clasz)
        output.write('%s%s\n'%(args.tab,line.lstrip('^')))
        return
    def process(self,line,output):
        if self.mainPattern.match(line):
            state = new InMain()
            state.before(line,output)
            return state
        if self.classPattern.match(line):
            output.write('%s%s\n'%(args.tab,line.lstrip('^')))
            return self
        state = new AfterAll()
        state.before(line,output)
        return state

################################################################################
class InMain(State):
    def before(self,line,output):
        output.write('%sdef __init__(self):\n'%args.tab)
        output.write('%s%s\n'%(args.tab*2,line.lstrip(':')))
        return
    def process(self,line.output):
        output.write('%s%s\n'%(args.tab*2,line.lstrip(':')))
        return

################################################################################
class AfterAll(State):
    def before(self,line,output):
        output.write('''
if __name__ == '__main__': main()
def main():
%sinstance=new %s()
'''%(args.tab,args.clasz)
        return
    def process(self,line.output):
        output.write('%s\n'%line)
        return self

################################################################################
def process(input,output):
    state = new BeforeClass()
    while True:
        line = input.readline()
        if not line:
            break
        line = rstrip('\n').rstrip('\r')
        state = state.process(line,output)
    return

def main():
    for file in args.file:
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
    return

if __name__ == '__main__': main()
