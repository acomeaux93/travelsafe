from app import db
from werkzeug.security import generate_password_hash, check_password_hash
# The class below is the one that allows for users to be remembered in session data
from datetime import datetime


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(64), index=True, unique=False)
    country_code = db.Column(db.String(64), index=True, unique=False)


class USState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    state = db.Column(db.String(64))
    positive = db.Column(db.String(64))
    positive_increase = db.Column(db.String(64))

    def __repr__(self):
        return f"State: {self.state}"


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2))
    date = db.Column(db.String(64))
    cases = db.Column(db.String(64))
    deaths = db.Column(db.String(64))
    recovered = db.Column(db.String(64))
