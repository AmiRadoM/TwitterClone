#   ┌-------------------------------------------------------┐
#   |   !!!IF YOU'RE MAKING ANY CHANGES IN THE MODELS!!!    |
#   |    make sure to run "migrate.sh" file in the repo     |
#   └-------------------------------------------------------┘

# models.py - all the definitions of the models in the database

from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(128))
    
    tweets = db.relationship("Tweet")

class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", overlaps="tweets")
    text = db.Column(db.String(280))