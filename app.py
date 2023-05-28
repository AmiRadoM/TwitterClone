# app.py - manages all of the initialization of flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

migrate = Migrate()

def create_app():
    # initializing the flask app
    app = Flask(__name__)
    app.secret_key = 'im secret'
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #initializing flask extentions
    db.init_app(app)
    migrate.init_app(app=app, db=db, render_as_batch=True)
    admin = Admin(app=app, template_mode='bootstrap3')

    #adding blueprints to the app
    from home import homeBP
    from api import apiBP
    app.register_blueprint(homeBP)
    app.register_blueprint(apiBP)

    #creating the database (if doesn't exist)
    import models
    if not path.exists(DB_NAME):
        db.create_all(app=app)

    #adding the models to the admin
    admin.add_view(ModelView(models.User, db.session))
    admin.add_view(ModelView(models.Tweet, db.session))
    
    return app