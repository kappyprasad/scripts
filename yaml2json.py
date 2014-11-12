#!/usr/bin/python

import os,re,sys,argparse,yaml,json

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-r','--reverse', action='store_true', help='reverse json->yaml')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    prettyPrint(vars(args), colour=True, output=sys.stderr)

def unicode_representer(dumper, uni):
    node = yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)
    return node

yaml.add_representer(unicode, unicode_representer)

def main():
    for file in args.file:
        with open(file) as fp:
            if args.reverse:
                object = json.loads(''.join(fp.readlines()))
                print yaml.dump(object)
            else:
                object = yaml.load(fp)
                print json.dumps(object)

if __name__ == '__main__': main()
