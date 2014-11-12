import praw, pprint

def main():
    user_agent = ("Karma breakdown by Nikhil Gupta")
    r = praw.Reddit(user_agent = user_agent)
    thing_limit = "none"
    user_name = "username" #replace username with your username
    user = r.get_redditor(user_name)
    gen = user.get_comments(limit=thing_limit)
    karma_by_subreddit = {}
    total = 0
    for thing in gen:
        subreddit = thing.subreddit.display_name
        karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)
        total += thing.score
    pprint.pprint(karma_by_subreddit) 
    print "Total karma is %i" % total

if __name__ == "__main__":
    main()
