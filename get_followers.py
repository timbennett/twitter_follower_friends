# Get the user IDs of everyone who follows a certain account,
# written into username.txt. 
#
# Usage: python get_followers.py username
#
# Twitter users have a screen name, which is changeable, and
# a user ID, which is permanent. This script returns the latter,
# because Twitter returns 5000 followers per query by this
# method, but many fewer if you want usernames. With an API
# limit of 15 requests per 15 minutes, this works out to
# 5000 followers a minute over the long term.

import sys
import tweepy
import csv
import twitter_auth

# make sure twitter_auth.py exists with contents:
#
#   access_key = ""
#   access_secret = ""
#   consumer_key = ""
#   consumer_secret = ""
#

# pick user to investigate
try:
    username = sys.argv[1]
except IndexError:
    print "Error: No username provided."
    raise
except:
    e = sys.exc_info()[0] 
    print "Error: General error {}".format(e)
    raise

print "Downloading followers for {}".format(username)

# set up authentication & api
auth = tweepy.OAuthHandler(twitter_auth.consumer_key, twitter_auth.consumer_secret)
auth.set_access_token(twitter_auth.access_key, twitter_auth.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

# zero out current followers file
ids_file = open('{}.txt'.format(username),'w')

# let's grab followers:
ids = []
for page in tweepy.Cursor(api.followers_ids, screen_name=username).pages():
    ids.extend(page)
    print "Downloaded {} followers".format(len(page))
    # write follower ids to file; check 
    x = 0
    ids_file = open('{}.txt'.format(username),'a')
    for user in page:
        ids_file.write("%s\n" % user)
        x += 1
    ids_file.close()
    print "Wrote {} followers to {}.txt".format(x, username)
    if len(page) != x:
        # Check previous issue, now thought fixed, where not all IDs would be written to file:
        print "Warning: some followers may have been missed.\nIDs expected: {}. IDs written:{}".format(len(ids),x)

print "Finished downloading."