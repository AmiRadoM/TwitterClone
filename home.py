# home.py - all the routes of the home blueprint

from flask import Blueprint, render_template, request
from sqlalchemy.sql import func

from models import Tweet, User

homeBP = Blueprint('home', __name__)

@homeBP.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@homeBP.route("/search")
def search():

    search = request.args.get("search").lower()

    tweets = []

    tweets_by_username = Tweet.query.join(Tweet.user).filter(func.lower(User.username).contains(search)).all()  
    tweets_by_text = Tweet.query.filter(func.lower(Tweet.text).contains(search)).all()

    tweets.extend([t.id for t in tweets_by_username])
    tweets.extend([t.id for t in tweets_by_text])

    tweets = list(dict.fromkeys(tweets))

    

    return render_template("search.html", tweets=tweets)

@homeBP.route("/about")
def about():
    return render_template("about.html")