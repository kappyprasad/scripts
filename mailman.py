#!/usr/bin/env python

import sys,os,re,json,argparse,poplib,imaplib,smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.parser import Parser

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',   action='store_true', help='show detailed output')
    parser.add_argument('-e','--encrypt',   action='store_true', help='use ssl')
    parser.add_argument('-u','--username',  action='store',      help='username',           default='eddo8888')
    parser.add_argument('-p','--password',  action='store',      help='password')

    parser.add_argument('-S','--server',    action='store',      help='server name',        default='mail.tpg.com.au')
    parser.add_argument('-P','--outport',   action='store',      help='out port number',    default=25,     type=int)
    parser.add_argument('-N','--inport',    action='store',      help='in port number',     default=110,    type=int)
    parser.add_argument('-T','--type',      action='store',      help='mailbox type',       default='POP3', choices=['IMAP','POP3'])

    parser.add_argument('-d','--delete',    action='store_true', help='delete after read')
    parser.add_argument('-m','--message',   action='store_true', help='show message')
    
    parser.add_argument('-a','--fromaddr',  action='store',      help='from email address', default='eddo888@tpg.com.au')
    parser.add_argument('-t','--recipient', action='store',      help='to email addresses', nargs='*')
    parser.add_argument('-j','--subject',   action='store',      help='subject')
    parser.add_argument('-b','--body',      action='store',      help='body')

    parser.add_argument('-o','--output',    action='store',      help='output file as body')
    parser.add_argument('-i','--input',     action='store',      help='input file as body')
    parser.add_argument('-f','--files',     action='store',      help='list of files',      nargs='*')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--read',      action='store_true', help='read email to directory')
    group.add_argument('-s', '--send',      action='store_true', help='send email')

    args = parser.parse_args()

    if args.verbose:
        sys.stderr.write('args: %s\n'%json.dumps(vars(args),indent=4))

    return args
    
keys = [ 'From', 'To', 'Subject', 'Date' ]

def readPOP3():
    if args.encrypt:
        poppy = poplib.POP3_SSL(args.server,args.inport)
    else:
        poppy = poplib.POP3(args.server,args.inport)

    poppy.user(args.username)
    poppy.pass_(password)
    numMessages = len(poppy.list()[1])
    print('Number of messages = %d'%numMessages)

    for m in range(numMessages):
        message =  poppy.retr(m+1)
        parser = Parser()

        jm = parser.parsestr('\n'.join(message[1]))
        
        if args.message:
            jsm = dict(payload=str(jm._payload))
            #print jm.keys()
            for key in keys:
                jsm[key] = jm.get(key)
            print json.dumps(jsm,indent=4)
        else:
            print jm['Subject'], jm.get_payload()
            
        if args.delete:
            poppy.dele(m+1)
            
    poppy.quit()
    return

def readIMAP():
    if args.encrypt:
        eye = imaplib.IMAP4_SSL(args.server, args.inport)
    else:
        eye = imaplib.IMAP4(args.server, args.inport)

    eye.login(args.username,password)

    if True:
        print( eye.list())
        
    while False:
        eye.select('inbox')

        if args.fromaddr:
            tipe, data = eye.search(None, 'FROM', '"%s"'%args.fromaddr)
        else:
            tipe, data = eye.search(None, 'ALL')

        #print data
        for num in data[0].split():
            tipe, data = eye.fetch(num, '(RFC822)')
            print (data[0][1])

    eye.close()
    eye.logout()
    
    return

def send():
    COMMASPACE = ', '

    msg = MIMEMultipart()
    msg['Subject'] = args.subject
    msg['From'] = args.fromaddr
    msg['To'] = COMMASPACE.join(args.recipient)

    if args.input:
        fp = open(args.input, 'rb')
        body = MIMEText(fp.read())
        fp.close()
        msg.attach(body)
    else:           
        msg.preamble = args.body

    if args.files:
        # Assume we know that the image files are all in PNG format
        for file in args.files:
            # Open the files in binary mode.  Let the MIMEImage class automatically
            # guess the specific image type.
            fp = open(file, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
    
    # Send the email via our own SMTP server.
    if args.encrypt:
        s = smtplib.SMTP_SSL(args.server,args.outport)
    else:
        s = smtplib.SMTP(args.server,args.outport)
    s.login(args.username, password)
    s.sendmail(args.fromaddr, args.recipient, msg.as_string())
    s.quit()
    return

def main():
    global args,password

    args = argue()

    if args.password:
        password = args.password
    else:
        passwords = Passwords(args.server, args.type, args.username, clear=False)
        password = passwords.password

    if args.read:
        if args.type == 'POP3':
            readPOP3()
        if args.type == 'IMAP':
            readIMAP()
    if args.send:
        send()

    return

if __name__ == '__main__': main()
