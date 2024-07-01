""" Another way to run the app"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  # Chemin relatif pour SQLite dans le dossier de l'application
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == "__main__":
    with app.app_context():

        print("Creating database tables...")
        db.create_all()
        print("Tables created.")

    app.run()
