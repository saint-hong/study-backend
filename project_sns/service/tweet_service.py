# business layer : create tweet and get tweet timeline for login user

class TweetService :
    
    ## dao : data access object from "model" layer
    def __init__(self, tweet_dao) :
        self.tweet_dao = tweet_dao
        
    def tweet(self, user_tweet) :
        ## user_id, tweet is parameter of "/tweet" endpoint
        tweet = user_tweet["tweet"]
        
        if len(tweet) > 300 :
            return None
        
        return self.tweet_dao.insert_tweet(user_tweet)
    
    def timeline(self, user_id) :
        ## user_id is parameter of "/timeline" endpoint
        return self.tweet_dao.get_timeline(user_id)