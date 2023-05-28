from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from home import homeBP

DB_NAME = "database.db"

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)

app.register_blueprint(homeBP)

app.run(host="0.0.0.0", port=5050, debug=True)