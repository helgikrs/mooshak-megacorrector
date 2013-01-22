#!/usr/bin/python2
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from time import gmtime, strftime

emails = ['hjaltmann@gmail.com', 'helgikrs@gmail.com']

def send_bug_report(message, corrector, submission):
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    
    curr_time = strftime("%d/%m/%Y %H:%M:%S", gmtime())
    message = """Corrector: %s
Time: %s
Submission: %s
Error message:
%s"""%(corrector, curr_time, submission, message)
    msg = MIMEText(message)

    me = 'mooshak@ru.is'
    msg['Subject'] = 'Mooshak corrector error [%s]'%curr_time
    msg['From'] = me
    msg['To'] = ', '.join(emails)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('smtp.ru.is')
    s.sendmail(me, emails, msg.as_string())
    s.quit()
