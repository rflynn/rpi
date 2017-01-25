#!/usr/bin/env python
# vim: set ts=4 et:

'''
send email via gmail using oauth so we don't have to store passwords

to generate an oauth token:
python util/xoauth.py --generate_oauth_token --user=your.email.address@gmail.com

ref: http://stackoverflow.com/questions/11445523/python-smtplib-is-sending-mail-via-gmail-using-oauth2-possible

NOTE: we're named email_ so we don't break import of python's email module!
'''

import oauth2 as oauth
import oauth2.clients.smtp as smtplib

class smtpconn:
    def __enter__(self):
        self.conn = smtplib.SMTP('smtp.googlemail.com', 587)
        return self.conn
    def __exit__(self, type, value, traceback):
        self.conn.close()

user = 'parseerror@gmail.com'
consumer = oauth.Consumer('anonymous', 'anonymous')
token = oauth.Token('1/*******************************************',
                    '************************')
url = 'https://mail.google.com/mail/b/' + user + '/smtp/'

def send_email(to='parse+error@gmail.com',
               subject='test',
               msg='msg'):
    with smtpconn() as conn:
        conn.set_debuglevel(True)
        conn.ehlo('test')
        conn.starttls()
        conn.ehlo()
        conn.authenticate(url, consumer, token)
        s = conn.sendmail(user, to,
                'To: ' + to + '\n' + \
                'From: ' + user + '\n' + \
                'Subject: ' + subject + '\n' + \
                '\n' + msg + '\n\n')
        return s

if __name__ == '__main__':
    send_email()

