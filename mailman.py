#!/usr/bin/env python

import sys, os, re, json, argparse, poplib, imaplib, smtplib, mimetypes

from datetime import datetime, timedelta
from dateutil import tz

from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser

from Tools.yokel import Yokel
from Tools.credstash import CredStash
from Tools.argue import Argue

yokel = Yokel()
credstash = CredStash()
args = Argue()

@args.argument(short='v',flag=True)
def verbose(): return

#=======================================================================================================================
@args.command(single=True)
class MailMan(object):

    @args.attribute(name='encrypt', short='e', flag=True)
    def _encrypt(self): return False

    @args.attribute(name='username', short='u')
    def _username(self): return

    @args.attribute(name='password', short='p')
    def _password(self): return

    @args.attribute(name='server', short='S')
    def _server(self): return

    @args.attribute(name='outport', short='P', type=int, default=25)
    def _outport(self): return

    @args.attribute(name='inport', short='N', type=int, default=110)
    def _inport(self): return

    @args.attribute(name='type', short='T', choices=['IMAP','POP3'], default='POP3')
    def _type(self): return
    
    def password(self):
        if self._password():
            return self._password()
        return credstash.get('%s:%s'%(self._server(),self._username()))
    
    #-------------------------------------------------------------------------------------------------------------------
    def payload(self,part,save=None):
        return  dict(
            payload=part.get_payload(),
            filename=part.get_filename(),
            type=part.get_content_type()
        )
    
    #-------------------------------------------------------------------------------------------------------------------
    def process(self, message, output=None, save=None):        
        parser = Parser()

        if verbose():
            print json.dumps(message,indent=4)

        jm = parser.parsestr(message)

        if jm:
            if verbose():
                json.dump(jm.keys(),sys.stderr,indent=4)
                
            payload = list()
            if jm.is_multipart():
                for part in jm.get_payload():
                    payload.append(self.payload(part,save=save))

            jsm = dict(preamble=jm.preamble,payload=payload)

            for key in ['To','From','Subject']:
                jsm[key] = jm.get(key)

            try:
                dt = yokel.time(jm['Date'])
                jsm['Date'] = dt.strftime(yokel.dts)
            except:
                jsm['Date'] = jm['Date']

            if output:
                print json.dumps(jsm,indent=4)
            else:
                print '{:<19} {:<20} -> {:<40}'.format(jsm['Date'][:19], jsm['From'][:20], jsm['Subject'][:40])

        else:
            sys.stderr.write('%s\n'%message)
            
        del parser

        return
    
    #-------------------------------------------------------------------------------------------------------------------
    @args.operation(name='read')
    def read(self, delete=False, output=False, save=None):
        '''
        read email from the server

        :param delete : delete after read
        :short delete : d
        :flag  delete : True

        :param output : output in json format
        :name  output : json
        :short output : j
        :flag  output : True

        :param save   : save email to this directory
        :short save   : s
        
        :returns None:

        '''

        if self._type() == 'POP3':

            if self._encrypt():
                poppy = poplib.POP3_SSL(_server(),_inport())
            else:
                poppy = poplib.POP3(self._server(),self._inport())

            poppy.user(self._username())
            poppy.pass_(self.password())
            numMessages = len(poppy.list()[1])
            sys.stderr.write('Number of messages = %d\n'%numMessages)

            if output:
                print '['
                
            for m in range(numMessages):
                if delete:
                    sys.stderr.write('\r%s'%(m+1))
                    sys.stderr.flush()
                    poppy.dele(m+1)
                    continue
                
                message =  poppy.retr(m+1)

                self.process('\n'.join(message[1]), output=output, save=save)
                
                if output and m+1 < numMessages:
                    print ','
            if output:
                print ']'
                
            poppy.quit()

        if self._type() == 'IMAP':
            
            if self._encrypt():
                eye = imaplib.IMAP4_SSL(self._server(), self._inport())
            else:
                eye = imaplib.IMAP4(self._server(), self._inport())

            eye.login(self._username(),self.password())

            if verbose():
                json.dump(eye.list(),sys.stderr,indent=4)

            eye.select('inbox')

            tipe, data = eye.search(None, 'ALL')
            
            #print data
            for num in data[0].split():
                tipe, data = eye.fetch(num, '(RFC822)')
                message = (data[0][1])
                self.process(message, output=output, save=save)

            eye.close()
            eye.logout()

        return

    #-------------------------------------------------------------------------------------------------------------------
    @args.operation(name='send')
    def send(self, fromaddr=None, recipients=[], subject=None, body=None, preamble=None, files=[]):
        '''
        send an email
 
        :param    fromaddr   : email sender address
        :short    fromaddr   : f
        :default  fromaddr   : eddo888@tpg.com.au

        :param    recipients : email recipient address
        :short    recipients : t
        :nargs    recipients : *
        :required recipients : True

        :param    subject    : email subject 
        :short    subject    : s
        :required subject    : True

        :param    body       : email body, @file or @- for stdin
        :short    body       : b
        :required body       : True

        :param    preamble   : some leading text in lieu of a body
        :short    preamble   : p

        :param    files      : path to files (assuming IMAGE type)
        :short    files      : a
        :nargs    files      : *

        '''

        COMMASPACE = ', '

        msg = MIMEMultipart()
        
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = COMMASPACE.join(recipients)

        if preamble:
            msg.preamble = preamble
        
        if body == '@-':
            with sys.stdin as fp:
                body = MIMEText(fp.read())
                msg.attach(body)
        elif body.startswith('@'):
            with open(body[1:], 'r') as fp:
                body = MIMEText(fp.read())
                msg.attach(body)
        else:
            bt = MIMEText(body)
            msg.attach(bt)

        for file in files:
            # Assume we know that the image files are all in PNG format
            # Open the files in binary mode.  Let the MIMEImage class automatically
            # guess the specific image type.

            ctype, encoding = mimetypes.guess_type(file)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(file) as fp:
                    # Note: we should handle calculating the charset
                    atch = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(file, 'rb') as fp:
                    atch = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(file, 'rb') as fp:
                    atch = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                with open(file, 'rb') as fp:
                    atch = MIMEBase(maintype, subtype)
                    atch.set_payload(fp.read())
                    # Encode the payload using Base64
                    encoders.encode_base64(atch)

            atch.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(atch)

        # Send the email via our own SMTP server.
        if self._encrypt():
            s = smtplib.SMTP_SSL(self._server(),self._outport())
        else:
            s = smtplib.SMTP(self._server(),self._outport())

        s.login(self._username(), self.password())
        s.sendmail(fromaddr, msg['To'], msg.as_string())
        s.quit()
            
        return

########################################################################################################################    
if __name__ == '__main__': args.execute()

