import praw, time, re, string
import smtplib
from smtplib import SMTP
from smtplib import SMTP_SSL
from smtplib import SMTPException
from email.mime.text import MIMEText

SUBJECT = "Laker Game Stream Links"
RECEIVER = "receiver@email.com"
SENDER = "sender@mail.com"
TEXT_SUBTYPE = "plain"

YAHOO_SMTP = "smtp.mail.yahoo.com" #I use yahoo for this example
YAHOO_SMTP_PORT = 465

r = praw.Reddit('Learning Python - NBA Stream Bot by Nikhil Gupta')
r.login('username', 'password')
title_flags = ['game', 'laker']
seen_comments = set()
streams = list()
#number = 1 #debugging

#print("Done setup") #debugging

while True:
    subreddit = r.get_subreddit('nba')
    for submission in subreddit.get_hot(limit=50):
        title = submission.title.lower()
        if all(submission in title for submission in title_flags):
            #print("Found submission") #debugging
            submission.replace_more_comments(limit=None, threshold=0)
            #print("Replaced comments") #debugging
            forest_comments = submission.comments
            #print("Forest comment format") #debugging
            #forest_comments.sort(key=ambda comment: comment.score) #Sorts by popularity, but not worth it for performance reasons
            #print "Sorted comments" #debugging
            for comment in forest_comments:
                if comment.id not in seen_comments and ("stream" in comment.body.lower() or "link" in comment.body.lower()):
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body)
                    for x in urls:
                        streams.append(x)
                seen_comments.add(comment.id)
            break #should only be 1 game thread, so need to continue looking

    #print("Searched through submissions") #debugging

    content = '\n'.join(streams)
    msg = MIMEText(content, TEXT_SUBTYPE)
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = RECEIVER

    try:
        smtpObj = SMTP_SSL(YAHOO_SMTP, YAHOO_SMTP_PORT)
        smtpObj.login(user=SENDER, password="password")
        smtpObj.sendmail(SENDER, RECEIVER, msg.as_string())
        smtpObj.quit();
        print ("Sent email")
    except SMTPException as error:
        print("ERROR: Unable to send mail")   
    
    ''' #debugging
    print "Done execution %i" % number
    number += 1
    #print len(relevant)
    '''
    #print "Done Executing"
    time.sleep(900)
