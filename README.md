# twitter_follower_friends
See who else a Twitter user's followers follow. For instance:

* Alice's followers are Bob, Chris and Dana.
* Bob also follows Chris, Eric and Ida.
* Chris also follows Eric, Frank, Gerald and Ida.
* Dana follows Harry, Ida and Jane.

These scripts let you discover that Alice's followers most often follow Ida and Eric:

| User   | Count |
|--------|-------|
| Ida    | 3     |
| Eric   | 2     |
| Chris  | 1     |
| Frank  | 1     |
| Gerald | 1     |
| Harry  | 1     |
| Jane   | 1     |

## Requirements

* Written for Python 2.7, probably needs adaptation for Python 3
* [Tweepy](http://www.tweepy.org/)

## Usage

1. [Create a Twitter app](https://apps.twitter.com/) and get the consumer key, consumer secret, access token and access token secret. Put these in twitter_auth.py.
2. Pick the account you want to investigate and gather its followers e.g. **python get_followers.py alice**
3. Sample the account's followers and get their friends e.g. **python sample_follower_friends.py alice 100 5000** which will get up to 5000 friends of 100 random Alice followers, outputting **alice_edges.csv**. Note: rate limiting means this will take one minute per follower examined.
4. Generate a list of user IDs and how many of Alice's followers follow them, and look up the usernames for the top 100 e.g. **python process_edges.py alice**

## get_followers.py

Get the user IDs of everyone who follows a certain account, written into username.txt. 

Usage: python get_followers.py username

Twitter users have a screen name, which is changeable, and a user ID, which is permanent. This script returns the latter, because Twitter returns 5000 followers per query by this method, but many fewer if you want usernames. With an API limit of 15 requests per 15 minutes, this works out to 5000 followers a minute over the long term.

## sample_follower_friends.py

Take a random sample of an account's followers, and find out who they follow.

Usage: python sample_follower_friends.py [username] [n followers] [n friends]

    Arguments:
    [username]:     A user whose followers you've previously collected. The
                    file username.txt must exist with one follower per line.
    [n followers]:  The number of [username]'s followers to sample. Limit is
                    15 requests per 15 minutes. Defaults to 15.
    [n friends]:    Number of friends to retrieve for each follower. Defaults
                    to 5000 (one page). You can set this much higher but if
                    you come across an account that follows a million people,
                    you'll be there all day grabbing its followers.

Output: [username]\_edges.csv, as [follower],[friend]

This script will append to any existing csv, so you can run it multiple times
without overwriting the results of previous runs. The next step is to run the
process_edges.py script to find the most frequently followed user IDs and name them.

## process_edges.py

Generate some intelligence from a list of who a user's followers follow.

Usage: python process_edges.py [username] [n]

    Arguments:
    [username]: a user previously examined with get_followers.py and
                sample_follower_friends.py. [username]_edges must exist.
    [n]:        Optional argument. For output purposes, create a file 
                containing just the users followed by more than [n] sampled 
                followers. Defaults to 50.
                
Output:

* [username]\_top.csv:     The usernames most followed by [username]'s followers. Four columns:
  * User ID: Unique across all Twitter users, not modifiable
  * Screen name: Unique across all Twitter users, but modifiable
  * Followers: number of sampled [username]'s followers who also follow this account
  * Fraction: fraction of sampled [username]'s followers who also follow this account
* [username]\_all.csv:     All users followed by [username]'s followers.
* [username]\_filtered.csv:All users followed by more than [n] followers.

## Example output:

###[@shanewarne](https://www.twitter.com/shanewarne):

| User ID | Screen name | Followers | Fraction |
|--------|-------|--------|-------|
| 135421739 | sachin_rt | 194 | 0.7185185185185186 |
| 71201743 | imVkohli | 161 | 0.5962962962962963 |
| 92724677 | virendersehwag | 142 | 0.5259259259259259 |
| 101311381 | iamsrk | 139 | 0.5148148148148148 |
| 132385468 | BeingSalmanKhan | 137 | 0.5074074074074074 |
| 121044171 | ImRaina | 134 | 0.4962962962962963 |
| 145125358 | SrBachchan | 130 | 0.48148148148148145 |
| 101695592 | deepikapadukone | 125 | 0.46296296296296297 |
| 88856792 | aamir_khan | 125 | 0.46296296296296297 |
| 45452226 | henrygayle | 125 | 0.46296296296296297 |

###[@billshortenmp](https://www.twitter.com/billshortenmp):

| User ID | Screen name | Followers | Fraction |
|--------|-------|--------|-------|
|	16734909	| TurnbullMalcolm | 677 | 0.6643768400392541 |
|	2768501	| abcnews | 624 | 0.6123650637880275 |
|	85436197	| JuliaGillard | 615 | 0.6035328753680078 |
|	93766096	| TonyAbbottMHR | 545 | 0.534838076545633 |
|	16832632	| MrKRudd | 529 | 0.5191364082433758 |
|	307755781	| tanya_plibersek | 507 | 0.4975466143277723 |
|	529147678	| SenatorWong | 480 | 0.47105004906771347 |
|	254515782	| AlboMP | 473 | 0.46418056918547596 |
|	813286	| BarackObama | 457 | 0.44847890088321885 |
|	16675569	| smh | 453 | 0.4445534838076546 |
