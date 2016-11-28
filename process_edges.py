''' 
Generate some intelligence from a list of who a user's followers follow.

Usage: python process_edges.py [username] [n]

    [username]: a user previously examined with get_followers.py and
                sample_follower_friends.py. [username]_edges must exist.
    [n]:        for output purposes, create a file containing just the
                users followed by more than [n] sampled followers.
                
Output:

    [username]_top.csv:     The usernames most followed by [username]'s followers.
    [username]_all.csv:     All users followed by [username]'s followers.
    [username]_filtered.csv:All users followed by more than [n] followers.

'''

import sys
import operator
import tweepy
import twitter_auth
import csv

# pick user to investigate
try:
    filename = "{}_edges.csv".format(sys.argv[1])
    print "Opening edge list {}".format(filename)
except IndexError:
    print "Error: No filename provided."
    raise
except:
    e = sys.exc_info()[0] 
    print "Error: General error {}".format(e)
    raise

# open the edge list    
with open(filename) as f:
    lines = f.read().splitlines()

# remove duplicate lines, which may occur if we ran sample_follower_friends.py
# multiple times and randomly selected the same user twice.
lines = list(set(lines))

# dictionary and list for counting purposes
friended_count = {}
follower_count = []

# count occurrences of friended users & followers
for line in lines:
    try:
         # if friend is in dict, add one to total
        friended_count[line.split(",")[1]] += 1
    except KeyError:
        # if friend not in dict, initialise with value 1
        friended_count[line.split(",")[1]] = 1

for line in lines:
    if line.split(",")[0] not in follower_count:
        follower_count.append(line.split(",")[0])

# reverse the dict
sorted = sorted(friended_count.items(), key=operator.itemgetter(1), reverse=True)
# the number of users checked:
print "Unique {} followers processed: {}".format(sys.argv[1], len(follower_count))

# Get the 100 most-followed user IDs, and convert numeric IDs to screen names:
analytics_dict = {} # dict to hold friended count and screen name
lookup_list = [] # list to hold IDs to look up screen names for
for user in sorted[1:101]: # sorted[0] will always be sys.argv[1], so skip it
    analytics_dict[int(user[0])] = [user[1]] # e.g. 10119182: [44]
    lookup_list.append(user[0])
auth = tweepy.OAuthHandler(twitter_auth.consumer_key, twitter_auth.consumer_secret)
auth.set_access_token(twitter_auth.access_key, twitter_auth.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)
lookup = api.lookup_users(user_ids=lookup_list)

for user in lookup:
    analytics_dict[user.id].append(user.screen_name) # e.g. 10119182: [44, u'J_Citizen']

# turn it all into a table-as-list, add a percentage-of-followers column, sort by count descending
final_list = []
for user in analytics_dict:
    final_list.append([user, analytics_dict[user][1], analytics_dict[user][0], analytics_dict[user][0]/float(len(follower_count))])
    final_list.sort(key=lambda elem: elem[2], reverse=True)

# Export the 100 top users:
with open("{}_top.csv".format(sys.argv[1]), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(final_list)    
print "Successfully exported top users."

# Now export all users and their count:
with open("{}_all.csv".format(sys.argv[1]), "wb") as f:
    writer = csv.writer(f)
    writer.writerows(sorted)
    
print "Successfully exported all users."

# Now export all edges where user count > n
try:
    n = sys.argv[2]
except:
    n = 50

all_user_dict = {}
for user in sorted:
    all_user_dict[int(user[0])] = [user[1]]
filtered_edges = []
for line in lines:
    user = int(line.split(",")[1])
    #print type(user)
    if all_user_dict[user][0] >= n:
        #print "including {} count {}".format(user, all_user_dict[user])
        filtered_edges.append(line)
#print filtered_edges
filtered_edge_count = 0
f = open("{}_filtered.csv".format(sys.argv[1]), "w")
for edge in filtered_edges:
    f.write("%s\n" % edge)
    filtered_edge_count +=1
f.close()
print "Successfully exported {} filtered edges with weight greater than {}.".format(filtered_edge_count, n)