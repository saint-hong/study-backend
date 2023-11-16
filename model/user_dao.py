# model layer call from user_service layer about user data

from sqlalchemy import text

class UserDao :
    
    def __init__(self, database) : 
        self.db = database
    
    ## call by create_new_user func in user_service layer : create_new_user()    
    def insert_user(self, user) : 
        with self.db.begin() as con :
            new_user_id = con.execute(text(
            """
            INSERT INTO users (name, email, profile, hashed_password)
                VALUES (:name, :email, :profile, :password) ;
            """), user).lastrowid
        
            return new_user_id
    
    ## call by get_user func in user_service layer : create_new_user()
    def get_user_data(self, id) : 
        with self.db.begin() as con :
            user_info = con.execute(text(
            """
            SELECT id, name, email, profile 
            FROM users
            WHERE id = :user_id ;
            """), {"user_id": int(id)}).fetchone()
            
            return {"id": user_info[0],
                    "name": user_info[1],
                    "email": user_info[2],
                    "profile": user_info[3]} if user_info else "empty"
    
    ## call by get_user func in user_service layer : login()
    def get_user_id_and_password(self, email) :
        with self.db.begin() as con : 
            id_pw = con.execute(text(
                """
                SELECT id, hashed_password
                FROM users
                WHERE email = :email ;
                """), {"email": email}).fetchone()
            
            return {"id": id_pw[0],
                    "hashed_password": id_pw[1]} if id_pw else "empty"
    
    ## call by user_service layer : follow()
    def insert_follow(self, user_id, follow_id) :
        with self.db.begin() as con :
            row = con.execute(text(
                """
                INSERT INTO users_follow_list (user_id, follow_user_id)
                       VALUES (:id, :follow) ;
                """), {"id": user_id, "follow": follow_id}).rowcount
            
            return row
    
    ## call by ser_service layer : unfollow()    
    def insert_unfollow(self, user_id, unfollow_id) : 
        with self.db.begin() as con :
            row = con.execute(text(
                """
                DELETE FROM users_follow_list
                WHERE user_id = :id
                AND follow_user_id = :unfollow ;
                """), {"id": user_id, "unfollow": unfollow_id}).rowcount
            
            return row
        
    ## call by user_service layer : save_profile_picture()
    def save_profile_picture(self, profile_pic_path, user_id) :
        
        ## insert pic path db
        with self.db.begin() as con :
            result = con.execute(text(
                """
                UPDATE users
                SET profile_picture = :profile_pic_path
                WHERE id = :user_id ;
                """), {'user_id': user_id, 'profile_pic_path': profile_pic_path}).rowcount
            
            return result
    
    ## call by user_service layer : get_profile_picture()
    def get_profile_picture(self, user_id) :
        
        with self.db.begin() as con :
            result = con.execute(text(
                """
                SELECT profile_picture
                FROM users
                WHERE id = :user_id ;
                """), {'user_id': user_id}).fetchone()
            
            return result[0] if result else 'empty'
        
    