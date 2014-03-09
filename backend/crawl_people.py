#a crawler which searches twitter to find all people tweeting about a certain keywords!
import tweepy
import sys
from pymongo import MongoClient

def clean_mong(db):
    #clean collections first
    db.users.remove()
    db.tweets.remove()

def connect_to_twitter():
    config = {}
    execfile("twitter.conf", config)
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)
    return api
 
def collect_tweets(query, db):
    ppl_no = 0
    try:
        clean_mong(db)
        api = connect_to_twitter()
        for status in tweepy.Cursor(api.search,
                           q=query,
                           rpp=100,
                           result_type="recent",
                           include_entities=True,
                           lang="en").items():
            author = status.author
            source = status.source
            text = status.text
            created_at = status.created_at
            #read user profile
            user = status.user
            description = status.user.description if status.user.description else ''
            user_id = status.user.id_str
            loc = status.user.location if status.user.location else ''
            name = status.user.name
            screen = status.user.screen_name
            url = status.user.url if status.user.url else ''
            avatar_image_url = status.user.profile_image_url
	    db.tweets.insert({"created_at": str(status.created_at), "author": str(status.author.screen_name), "source": str(status.source), "text": str(status.text)})
            if db.users.find({"screen": screen}).count() == 0:
                db.users.insert({"avatar_image_url": avatar_image_url, "description": description, "id_str": user_id, "location" : loc, "name": name, "screen" : screen, "url": url})
                ppl_no += 1
    except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            print e
            pass
    return ppl_no
