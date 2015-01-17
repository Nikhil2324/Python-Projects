import praw, time, re, string
import smtplib
from smtplib import SMTP
from smtplib import SMTP_SSL
from smtplib import SMTPException
from email.mime.text import MIMEText

SUBJECT = "Fresh Hip-Hop Links"
RECEIVER = "receivingEmail.com"
SENDER = "sendingEmail.com"
TEXT_SUBTYPE = "plain"

YAHOO_SMTP = "smtp.mail.yahoo.com"
YAHOO_SMTP_PORT = 465

r = praw.Reddit('Fresh Rap Stream by Nikhil Gupta')
r.login('redditUsername', 'redditPassword')
title_flags = ['fresh']
seen_comments = set()
NUMBER = 1

def getLinks():
    fresh = {}
    subreddit = r.get_subreddit("hiphopheads")
    for submission in subreddit.get_hot(limit=50):
        title = submission.title.lower()
        if all(submission in title for submission in title_flags):
            title = submission.title.encode('utf-8') #some characters outside of ASCII range, need to encode
            link = submission.url.encode('utf-8') #some characters outside of ASCII range, need to encode
            fresh[title] = link
            
    content = "Fresh Streams\n\n"
    for i in fresh:
        content += (i + '\n' + fresh[i] + '\n\n')

    msg = MIMEText(content, TEXT_SUBTYPE)
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    try:
        smtpObj = SMTP_SSL(YAHOO_SMTP, YAHOO_SMTP_PORT)
        smtpObj.login(user=SENDER, password="emailPassword")
        smtpObj.sendmail(SENDER, RECEIVER, msg.as_string())
        smtpObj.quit();
        print ("Sent email")
        
    except SMTPException as error:
        print("ERROR: Unable to send mail")
    
    time.sleep(900)

def main():
    while True:
        getLinks()

if __name__ == '__main__':
    main()

#Implement timing functionality
