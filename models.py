#   ┌-------------------------------------------------------┐
#   |   !!!IF YOU'RE MAKING ANY CHANGES IN THE MODELS!!!    |
#   |    make sure to run "migrate.sh" file in the repo     |
#   └-------------------------------------------------------┘

# models.py - all the definitions of the models in the database

from flask_login import UserMixin

from sqlalchemy.sql import func

from app import db

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(128))
    
    tweets = db.relationship("Tweet", cascade="all, delete")
    likes = db.relationship("Like", cascade="all, delete")

    def __commit_delete__(self):
        print("Deleted User")

class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", overlaps="tweets")
    text = db.Column(db.String(280))
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    #TODO add likes to tweets (show the number of likes on the tweet and for each user the abillity to see their liked tweets)
    likes = db.relationship("Like", cascade="all, delete")

class Like(db.Model):
    __tablename__ = "like"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", overlaps="likes")
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    tweet = db.relationship("Tweet", overlaps="likes")