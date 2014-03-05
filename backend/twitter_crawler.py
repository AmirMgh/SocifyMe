import tweepy
import unittest
import sys

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
config = {}
execfile("twitter.conf", config)

consumer_key = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token = config["access_token"]
access_token_secret = config["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

class TwitterCrawlerAPI:
    def __init__(self):
        self.api = tweepy.API(auth)

    #get all methods for tweepy api
    def getMethods(self):
        methods = [method for method in dir(tweepy.api) if callable(getattr(tweepy.api, method))]
        return methods

    #Rate Limit Object

    #get API limit
    def getApiLimit(self):
        return self.api.rate_limit_status()

    #get method limit
    def getApiMethodLimit(self, apiLimit, methodName):
        resources = apiLimit['resources']

        try:
            user = resources['users'][methodName]
            return user['remaining']
        except KeyError, e:
            pass

        try:
            status = resources['statuses'][methodName]
            return status['remaining']
        except KeyError, e:
            pass

        try:
            application = resources['application'][methodName]
            return application['remaining']
        except KeyError, e:
            pass

        return None

    #User Object

    #get user object
    def getUser(self, twitter_handle):
        try:
            user = self.api.get_user(twitter_handle)
        except:
            return None
        return user

    #get twitter account creation time
    def getUserCreatedAt(self, user):
        return user.created_at.strftime('%a %Y-%m-%d %H:%M:%S')

    #default profile
    def isUserDefaultProfile(self, user):
        if not user.default_profile:
            return False
        return True

    #default profile img
    def isUserDefaultProfileImg(self, user):
        if not user.default_profile_image:
            return False
        return True

    #get description
    def getUserDescription(self, user):
        return user.description

    #get fav count
    def getUserFavCnt(self, user):
        return user.favourites_count

    #get followers list
    def getUserFollowers(self, user):
        return user.followers()

    #get friends
    def getUserFriends(self, user):
        return user.friends()

    #get follower ids
    def getUserFollowerIds(self, user):
        return user.followers_ids()

    #get no of followers
    def getUserFollowersCount(self, user):
        return user.followers_count

    def getUserFriendsCount(self, user):
        return user.friends_count

    #get name
    def getUserName(self, user):
        return user.name

    #get location
    def getUserLocation(self, user):
        return user.location

    #get screen name
    def getUserScreenName(self, user):
        return user.screen_name

    #get utc offset
    def getUserUTCOffset(self, user):
        return user.utc_offset

    #get time zone
    def getUserTimeZone(self, user):
        return user.time_zone

    #get geo enabled
    def getUserGeoEnabled(self, user):
        return user.geo_enabled

    #get user id
    def getUserIDString(self, user):
        return user.id_str

    #get user language
    def getUserLanguage(self, user):
        return user.lang

    #get user protected
    def getUserProtected(self, user):
        return user.protected

    #get user statuses or tweets count
    def getUserStatusesCount(self, user):
        return user.statuses_count

    #get user url
    def getUserURL(self, user):
        return user.url

    #is user verified
    def isUserVerified(self, user):
        return user.verified
    
    #get profile bg img url
    def getUserProfBGImgUrl(self, user):
        return user.profile_background_image_url

    #get profile banner url (this attribute might not appear on some accounts, 
    #and an exception will be thrown)
    def getUserProfBannerUrl(self, user):
        return user.profile_banner_url

    #is user using prof bg img
    def isUserProfBGImg(self, user):
        return user.profile_use_background_image

    #Tweet Object

    #get timeline
    def getTimeline(self, twitter_handle, numOfTweet):
        return self.api.user_timeline(screen_name = twitter_handle, count = numOfTweet)

    #get author, which is an object of user
    def getStatusAuthor(self, status):
        return status.author.screen_name

    #get author id string
    def getStatusAuthorIDString(self, status):
        return status.author.id_str

    #get tweet created timestamp
    def getStatusCreatedAt(self, status):
        return status.created_at.strftime('%a %Y-%m-%d %H:%M:%S')

    #get tweet favourite count
    def getStatusFavoriteCount(self, status):
        return status.favorite_count

    #get tweet coordinates
    def getStatusCoordinates(self, status):
        return status.coordinates

    #get tweet id
    def getStatusIDString(self, status):
        return status.id_str

    #get tweet language
    def getStatusLanguage(self, status):
        return status.lang

    #get retweet count
    def getStatusRetweetCount(self, status):
        return status.retweet_count

    #get tweet source
    def getStatusSource(self, status):
        return status.source

    #get tweet source url
    def getStatusSourceURL(self, status):
        return status.source_url

    #get tweet text
    def getStatusText(self, status):
        return status.text

    #get geo info
    def getStatusGeo(self, status):
        return status.geo

    #check if there is a unidirectional or bi-directional link
    def checkLink(self, src_name, tgt_name):
        source, target = self.api.show_friendship(source_screen_name = src_name, target_screen_name = tgt_name)
        if source.followed_by:
            print "%s followed by %s" % (source.screen_name, target.screen_name)
        if source.following:
            print "%s following %s" % (source.screen_name, target.screen_name)
        if target.followed_by:
            print "%s followed by %s" % (target.screen_name, source.screen_name)
        if target.following:
            print "%s following %s" % (target.screen_name, source.screen_name)

    def runCrawler(self, twitter_handle, db):
        user = self.getUser(twitter_handle)
        profile = {}
        if not user:
            return False
        profile["screen"] = twitter_handle
        profile["id_str"] = self.getUserIDString(user) 
        profile["location"] = self.getUserLocation(user).encode('utf-8')
        profile["name"] = self.getUserName(user).encode('utf-8')
        profile["description"] = self.getUserDescription(user).encode('utf-8')
        profile["url"] = self.getUserURL(user)
        db.socifiers.insert({"description": profile["description"], "id_str": profile["id_str"], "location" : profile["location"], "name": profile["name"], "screen" : profile["screen"], "url": profile["url"]})
        return True

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print 'Usage: ' + sys.argv[0]
        sys.exit(1)
    twitter = TwitterCrawlerAPI()
    twitter_handle = "kjahanbakhsh"
    profile = twitter.runCrawler(twitter_handle)
    #print profile
