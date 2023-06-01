# api.py - all the routes of the API

from flask import Blueprint, request, jsonify, Response, send_file
from flask_login import login_required, current_user

import json
import random
from datetime import datetime
import os

from models import db, Tweet, User, Like
import utils

apiBP = Blueprint('api', __name__, url_prefix="/api")

@apiBP.route("/post-tweet", methods=["POST"])
@login_required
def post_tweet():
    # post a tweet
    # gets: [text: str (the text in the tweet)]

    data = json.loads(request.data)

    if(len(data["text"].rstrip().lstrip()) > 280):
        return Response("Tweet text exceeded 280 characters", 400)
    elif(data["text"].strip() == ""):
        return Response("Tweet is empty", 400)
 
    newTweet = Tweet(text=data["text"].rstrip().lstrip(), user_id=current_user.id)
    db.session.add(newTweet)
    db.session.commit()

    return jsonify({"done": True})

@apiBP.route("/get-tweet", methods=["POST"])
def get_tweet():
    # get a tweets data by its id
    # gets: [tweet_id: int (the id of the tweet)]

    tweet_id = json.loads(request.data)["tweet_id"]

    tweet = Tweet.query.get(tweet_id)

    tweet_age = datetime.utcnow() - tweet.time

    if(int(tweet_age.days) > 0): # Days
        time_ago = tweet.time.strftime("%B %d %Y")
    elif(int(tweet_age.seconds / 3600) > 0): # Hours
        time_ago = str(int(tweet_age.seconds / 3600)) + " hour" + ("s" if int(tweet_age.seconds / 3600) != 1 else "") + " ago"
    elif(int(tweet_age.seconds / 60) > 0): # Minutes
        time_ago = str(int(tweet_age.seconds / 60)) + " minute" + ("s" if int(tweet_age.seconds / 60) != 1 else "") + " ago"
    else: # Seconds (just say now)
        time_ago = "now"

    liked = False
    if(current_user.is_authenticated):
        if(Like.query.filter_by(user_id = current_user.id, tweet_id=tweet_id).first()):
            liked = True

    return jsonify({"user_id": tweet.user_id, "text": tweet.text, "time_ago": time_ago, "likes": len(tweet.likes), "liked": liked})

@apiBP.route("/like-tweet", methods=["POST"])
@login_required
def like_tweet():
    # give a tweet a like
    # gets: [tweet_id: int (the id of the tweet)]

    tweet_id = json.loads(request.data)["tweet_id"]

    possible_like = Like.query.filter_by(user_id=current_user.id, tweet_id=tweet_id).first() #looking for a like that already exists

    if possible_like:
        # deleting the like
        db.session.delete(possible_like)
    else:
        # creating the like
        newLike = Like(user_id = current_user.id, tweet_id = tweet_id)
        db.session.add(newLike)
    
    db.session.commit()

    return jsonify({"done": True}) 

@apiBP.route("/recommend-tweets", methods=["POST"])
def recommend_tweets():
    # recommends tweets (for now just sends random tweets)
    # gets: [user_id: int (the id of the user), amount: int (how many tweets to recommend)]

    data = json.loads(request.data)

    maxIndex = Tweet.query.count()
    tweets = random.sample([*range(1, maxIndex+1)], utils.clamp(data["amount"],0,maxIndex))

    return jsonify({"tweets": tweets})

@apiBP.route("/profile", methods=["POST"])
def profile():
    # get a profile data by user id
    # gets: [user_id: int (the id of the user)]

    user_id = str(json.loads(request.data)["user_id"])

    user = User.query.get(user_id)

    return jsonify({"username": user.username, "email": user.email})

@apiBP.route("/pfp", methods=["POST"])
def pfp():
    # get a profile picture by user id
    # gets: [user_id: int (the id of the user)]

    user_id = str(json.loads(request.data)["user_id"])

    from app import UPLOAD_PATH
    if(not os.path.exists(UPLOAD_PATH + f"/pfp/{user_id}.jpg")):
        return Response("No profile picture", 500)

    return send_file(UPLOAD_PATH + f"/pfp/{user_id}.jpg", mimetype="image/jpg")