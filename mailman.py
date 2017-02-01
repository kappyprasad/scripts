#!/usr/bin/env python

import sys,os,re,json,argparse,poplib,imaplib,smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.parser import Parser

from Tools.argue import Argue

args = Argue()

#=======================================================================================================================
@args.command(single=True)
class MailMan(object):

    @args.function(name='encrypt', short='e', flag=True)
    def _encrypt(self): return False

    @args.function(name='username', short='u')
    def _username(self): return 'eddo8888'

    @args.function(name='password', short='p')
    def _password(self): return

    @args.function(name='server', short='S')
    def _server(self): return 'mail.tpg.com.au'

    @args.function(name='outport', short='P', type=int)
    def _outport(self): return 25

    @args.function(name='inport', short='N', type=int)
    def _inport(self): return 110

    @args.function(name='type', short='T', choices=['IMAP','POP3'])
    def _type(self): return 'POP3'
    
    @args.function(name='output', short='o')
    def _output(self): return

    @args.function(name='input', short='i')
    def _input(self): return

    #-------------------------------------------------------------------------------------------------------------------
    @args.operation(name='read')
    def read(self, delete=False, show=False):
        '''
        read email from the server
        :param delete boolean to delete after read
        :param show boolean to show full message
        :returns None
        '''
        
        if self._type() == 'POP3':

            if self._encrypt():
                poppy = poplib.POP3_SSL(_server(),_inport())
            else:
                poppy = poplib.POP3(self._server(),self._inport())

            poppy.user(self._username())
            poppy.pass_(self._password())
            numMessages = len(poppy.list()[1])
            print('Number of messages = %d'%numMessages)

            for m in range(numMessages):
                message =  poppy.retr(m+1)
                parser = Parser()

                jm = parser.parsestr('\n'.join(message[1]))

                if message:
                    jsm = dict(payload=str(jm._payload))
                    for key in ['To','Date','From','Subject']:
                        jsm[key] = jm.get(key)
                        print json.dumps(jsm,indent=4)
                else:
                    print jm['Subject'], jm.get_payload()

                if delete:
                    poppy.dele(m+1)

            poppy.quit()

        if self._type() == 'IMAP':
            
            if self._encrypt():
                eye = imaplib.IMAP4_SSL(self._server(), self._inport())
            else:
                eye = imaplib.IMAP4(self._server(), self._inport())

            eye.login(self._username(),self._password())

            if True:
                print( eye.list())

            while False:
                eye.select('inbox')

                if self._fromaddr():
                    tipe, data = eye.search(None, 'FROM', '"%s"'%self._fromaddr())
                else:
                    tipe, data = eye.search(None, 'ALL')

                #print data
                for num in data[0].split():
                    tipe, data = eye.fetch(num, '(RFC822)')
                    print (data[0][1])

            eye.close()
            eye.logout()

        return

    #-------------------------------------------------------------------------------------------------------------------
    @args.operation(name='send')
    def send(self, fromaddr, recipient, subject, body, file):

        COMMASPACE = ', '

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = COMMASPACE.join(recipient)

        if self._input():
            fp = open(self._input(), 'rb')
            body = MIMEText(fp.read())
            fp.close()
            msg.attach(body)
        else:           
            msg.preamble = body

        if file:
            # Assume we know that the image files are all in PNG format
            # Open the files in binary mode.  Let the MIMEImage class automatically
            # guess the specific image type.
            fp = open(file, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)

        # Send the email via our own SMTP server.
        if self._encrypt():
            s = smtplib.SMTP_SSL(self._server(),self._outport())
        else:
            s = smtplib.SMTP(self._server(),self._outport())
            s.login(self._username(), self._password())
            s.sendmail(fromaddr, recipient, msg.as_string())
            s.quit()
            
        return

########################################################################################################################    
if __name__ == '__main__': args.execute()

