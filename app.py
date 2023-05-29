# app.py - manages all of the initialization of flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
UPLOAD_PATH = "./static/upload"

migrate = Migrate()

def create_app():
    # initializing the flask app
    app = Flask(__name__)
    app.secret_key = 'im secret'
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
    app.config['MAX_CONTENT_PATH'] = 6000000

    # initializing flask extentions
    db.init_app(app)
    migrate.init_app(app=app, db=db, render_as_batch=True)
    admin = Admin(app=app, template_mode='bootstrap3')
    lm = LoginManager(app)

    # adding blueprints to the app
    from home import homeBP
    from api import apiBP
    from auth import authBP
    app.register_blueprint(homeBP)
    app.register_blueprint(apiBP)
    app.register_blueprint(authBP)

    # creating the database (if doesn't exist)
    import models
    if not path.exists(DB_NAME):
        db.create_all(app=app)

    # adding the models to the admin
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.Tweet, db.session))

    # initiating the LoginManager
    @lm.user_loader
    def load_user(user_id):
        return models.User.query.get(user_id)
    
    return app