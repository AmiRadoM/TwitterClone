# api.py - all the routes of the API

from flask import Blueprint, request, jsonify, Response

import json

from models import db, Tweet

apiBP = Blueprint('api', __name__, url_prefix="/api")

@apiBP.route("/post-tweet", methods=["POST"])
def post_tweet():
    #post a tweet

    data = json.loads(request.data)

    if(len(data["text"]) > 280):
        return Response("Tweet text exceeded 280 characters", 400)

    #TODO associate tweet to a user    
    newTweet = Tweet(text=data["text"])
    db.session.add(newTweet)
    db.session.commit()

    return jsonify({"done": True})