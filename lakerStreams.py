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

while True:
    subreddit = r.get_subreddit('nba')
    for submission in subreddit.get_hot(limit=50): #get 50 most popular posts at the moment (game threads are usually popular, if not in the top 50, they haven't been created yet)
        title = submission.title.lower()
        if all(submission in title for submission in title_flags): #if the submission title has 'laker' and 'game' in it, it is the game thread
            submission.replace_more_comments(limit=None, threshold=0) #get ALL the comments (just in case some links are buried)
            forest_comments = submission.comments
            #forest_comments.sort(key=lambda comment: comment.score) #Sorts by popularity, but not worth it for performance reasons in my opnion
            for comment in forest_comments:
                if comment.id not in seen_comments and ("stream" in comment.body.lower() or "link" in comment.body.lower()):
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment.body) #regex magic to find links in the html source
                    for x in urls:
                        streams.append(x) #each x is a link, put it in the list
                seen_comments.add(comment.id)
            break #should only be 1 game thread, so need to continue looking

    content = '\n'.join(streams) #join each link with a newline
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
    
    time.sleep(900) #wait 15 minutes, see if new links are there
