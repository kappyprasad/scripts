#!/usr/bin/env python2.7

import sys,os,re,xmltodict,argparse,json,vobject,datetime

parser = argparse.ArgumentParser('Convert microsoft .contact to .vcard')

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-o','--output',  action='store',      help='output dir', default='vcards')
parser.add_argument('emails', action='store', help='file containing comma seperated email addresses')

args = parser.parse_args()

companies = {
    'qantasloyalty.com'          : 'Qantas Loyalty',
    'intelligentpathways.com.au' : 'Intelligent Pathways',
    'bcgdv.com'                  : 'BCG Digital Ventures',
}

if args.verbose:
    sys.stderr.write('args:')
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

def convert(fqn):
    triangles = re.compile('^([^<]+) <([^>]+)>$')
    match = triangles.match(fqn)
    if not match:
        sys.stderr.write('triangles failed=%s\n'%fqn)
        return

    names = match.group(1).split(' ')
    email = match.group(2)
    
    vcard = vobject.vCard()
    vcard.add('n')

    if len(names) == 1:
        vcard.n.value = vobject.vcard.Name(
            given      = names[0],
            additional = '',
            family     = '',
        )
    if len(names) == 2:
        vcard.n.value = vobject.vcard.Name(
            given      = names[0],
            additional = '',
            family     = names[1],
        )
    if len(names) == 3:
        vcard.n.value = vobject.vcard.Name(
            given      = names[0],
            additional = names[1],
            family     = names[2]
        )
    if len(names) > 3:
        sys.stderr.write('error names=%s\n'%names)

    vcard.add('fn')
    vcard.fn.value = ' '.join(names)

    domains = re.compile('^([^@]+)@(.*)$')
    match = domains.match(email)
    if not match:
        sys.stderr.write('domains failed=%s'%email)
        return

    company = match.group(2)

    if company in companies.keys():
        company = '%s'%companies[company]
        
    vcard.add('org')
    vcard.org.value = [ company ]
    
    ve = vcard.add('email')
    ve.value = email
        
    vcard.prettyPrint()

    target = '%s.vcf'%' '.join(names)
    if args.output:
        target = '%s/%s'%(args.output,target)
        
    output = open(target,'w')
    vcard.serialize(buf=output)
    output.close()
    return

def main():
    if args.output and not os.path.isdir(args.output):
        os.makedirs(args.output)

    input = open(args.emails)
    emails=''.join(map(lambda x : x.replace('\r','').replace('\n',''), input.readlines()))
    for email in emails.split(','):
        convert(email)
    input.close()

    return

if __name__ == '__main__': main()
