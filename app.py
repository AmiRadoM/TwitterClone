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
    app = Flask(__name__)
    app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    migrate.init_app(app=app, db=db, render_as_batch=True)

    admin = Admin(app=app, template_mode='bootstrap3')

    from home import homeBP

    app.register_blueprint(homeBP)

    import models

    if not path.exists(DB_NAME):
        db.create_all(app=app)

    admin.add_view(ModelView(models.User, db.session))
    
    return app