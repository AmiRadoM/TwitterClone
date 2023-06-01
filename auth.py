# auth.py - all the routes of the authentication methods

from flask import Blueprint, render_template, request, redirect, url_for, Response, flash
from flask_login import login_user, logout_user, login_required

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from validate_email import validate_email
from usernames import is_safe_username
import os

from models import db, User

authBP = Blueprint('auth', __name__, url_prefix="/auth")

@authBP.route("/login", methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        data = request.form

        email = data.get("email").lower()
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if not user:
            flash(f"Couldn't find account for {email}", "error")
        elif not check_password_hash(user.password, password):
            flash("Password is incorrect", "error")           
        else:
            login_user(user)
            return redirect(url_for("home.home"))     
            
    return render_template("login.html")

@authBP.route("/signup", methods=["GET", "POST"])
def signup():
    if(request.method=="POST"):
        data = request.form

        username = data.get("username")
        email = data.get("email").lower()
        password = data.get("password")
        f = request.files['pfp']
        fName = secure_filename(f.filename)
        fFormat = os.path.splitext(fName)[1]

        print(f)

        if(len(password) < 8):
            flash("Password needs to be at least 8 characters long", "error")
        elif(len(password) > 128):
            flash("Password needs to be less than 128 characters long", "error")
        elif(len(email) > 320):
            flash("Email is invalid", "error")
        elif(not validate_email(email)):
            flash("Email is invalid", "error")
        elif(User.query.filter_by(email=email).first() != None):
            flash("Email is already in use", 'error')
        elif len(username) > 15 or len(username) < 4:
            flash("Username length should be 4-15 characters long", "error")
        elif not is_safe_username(username):
            flash("Username isn't appropriate (Should include english characters)", "error")
        elif(User.query.filter_by(username=username).first() != None):
            flash("Username is already in use", 'error')
        elif fName != '' and fFormat not in ['.png', '.jpg', '.jpeg']:
            flash("Profile picture needs to be in the following formats: .png, .jpg, .jpeg", 'error')
        else:
            newUser = User(username=username, email = email, password=generate_password_hash(password, method='sha256'))
            db.session.add(newUser)
            db.session.commit()
            if(fName != ''):
                from app import UPLOAD_PATH
                f.save(UPLOAD_PATH + f"/pfp/{newUser.id}.jpg")
            
            login_user(newUser)
            return redirect(url_for("home.home"))

    return render_template("signup.html")

@authBP.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))