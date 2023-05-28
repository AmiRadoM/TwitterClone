from main import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.integer, primary_key=True)
