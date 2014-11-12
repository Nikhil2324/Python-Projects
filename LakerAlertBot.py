import praw, time

r = praw.Reddit('Learning Python - PRAW related question monitor by BeezInTheTrap')
r.login('BeezInTheTrap', 'air23jordan')
already_done = []
count = 1;

prawWords = ['laker', 'kobe']

while True:
    subreddit = r.get_subreddit('nba')
    for submission in subreddit.get_hot(limit=10):
        op_text = submission.selftext.lower()
        op_title = submission.title.lower()
        has_praw = (any(string in op_text for string in prawWords) or any(string in op_title for string in prawWords))
        if submission.id not in already_done and has_praw:
            msg = '[Laker Thread](%s)' % submission.short_link
            r.send_message('BeezInTheTrap', 'Laker Fan Alert', msg)
            already_done.append(submission.id)
    print "Done Execution #%i" % count
    count += 1
    time.sleep(1800)
