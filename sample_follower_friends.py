'''
Take a random sample of an account's followers, and find out who they follow.

Usage: python sample_follower_friends.py [username] [n followers] [n friends]

    [username]:     A user whose followers you've previously collected. The
                    file username.txt must exist with one follower per line.
    [n followers]:  The number of [username]'s followers to sample. Limit is
                    15 requests per 15 minutes. Defaults to 15.
    [n friends]:    Number of friends to retrieve for each follower. Defaults
                    to 5000 (one page). You can set this much higher but if
                    you come across an account that follows a million people,
                    you'll be there all day grabbing its followers.

Output: [username]_edges.csv, as [follower],[friend]

This script will append to any existing csv, so you can run it multiple times
without overwriting the results of previous runs. The next step is to run the
process_edges.py script to find the most frequently followed user IDs and name them.
'''

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

# set up authentication & api
auth = tweepy.OAuthHandler(twitter_auth.consumer_key, twitter_auth.consumer_secret)
auth.set_access_token(twitter_auth.access_key, twitter_auth.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

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
    
# number of users to fetch
try:
    follower_count = int(sys.argv[2])
except:
    follower_count = 15
    
# number of friends to fetch
try:
    friend_limit = int(sys.argv[3])
except:
    friend_limit = 5000
     
print "Getting up to {} friends of {} random {} followers...".format(friend_limit, follower_count, username)

# load pre-existing followers
try:
    filename = "{}.txt".format(username)
    print "Reading followers from {}...".format(filename)
    with open(filename) as f:
        ids = f.read().splitlines()
    print "Imported {} follower IDs...".format(len(ids))
except:
    print "Could not open {}.txt, does it exist? Run get_followers.py first.".format(username)
    raise

def get_friends_list(user_id, limit=5000):
    '''
    Get [limit] friends for the given user_id
    '''
    following = []
    for page in tweepy.Cursor(api.friends_ids, user_id=user_id, count=limit).pages():
        following.extend(page)
        print "{} follows {} people".format(user_id, len(following))
        if len(following) >= limit: # don't get more than this number of followers
            break
    return following

# get a random selection of the user's followers  
import random
followers_to_check = random.sample(ids,follower_count)

# check each follower's friends
for follower in followers_to_check:
    friend_dict = {} # 
    try:
        following = get_friends_list(follower, friend_limit)
        friend_dict[follower] = following
        # construct an edge list (suitable for gephi), appending it to the previous ones
        edge_list = []
        for follower in friend_dict:
            for friend in friend_dict[follower]:
                edge_list.append("{},{}".format(follower,friend))
        edge_file = open('{}_edges.csv'.format(username),'a')
        for edge in edge_list:
            edge_file.write("%s\n" % edge)
        edge_file.close()
    except: #maybe account is private
        print "Error (possibly private):", follower
