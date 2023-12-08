# model layer call from tweet_service layer about tweet data

from sqlalchemy import text

class TweetDao :
    
    def __init__(self, database) :
        self.db = database
        
    def insert_tweet(self, user_tweet) : 
        with self.db.begin() as con :
            row = con.execute(text(
                """
                INSERT INTO tweets (user_id, tweet)
                       VALUES (:id, :tweet) ;
                """), user_tweet).rowcount
            
            return row
        
    def get_timeline(self, user_id) :
        with self.db.begin() as con :
            rows = con.execute(text(
                """
                SELECT user_id, tweet
                FROM tweets
                WHERE user_id IN (SELECT follow_user_id FROM users_follow_list WHERE user_id = :id)
                OR user_id = :id ;
                """), {"id": int(user_id)}).fetchall()
            
            timeline = [{"user_id": row[0], "tweet": row[1]} for row in rows]
            
            return timeline
        
