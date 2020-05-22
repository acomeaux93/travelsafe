from app import db
from werkzeug.security import generate_password_hash, check_password_hash
#The class below is the one that allows for users to be remembered in session data
from datetime import datetime


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(64), index=True, unique=False)
    country_code = db.Column(db.String(64), index=True, unique=False)

class USState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(64))
    clean_date = db.Column(db.String(64))
    state = db.Column(db.String(64))
    positive = db.Column(db.String(64))
    positive_increase = db.Column(db.String(64))

    def __repr__(self):
        return f"State: {self.state}"


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(2))
    date = db.Column(db.String(64))
    clean_date = db.Column(db.String(64))
    cases = db.Column(db.String(64))
    deaths = db.Column(db.String(64))
    recovered = db.Column(db.String(64))

class USReference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_state_name = db.Column(db.String(64))
    state_abbreviation = db.Column(db.String(2))
    state_population = db.Column(db.Integer())

class LocationRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_location = db.Column(db.String(64))
    to_location = db.Column(db.String(64))
    timestamp = db.Column(db.String(64))

class AlertRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alert_location = db.Column(db.String(64))
    form_data = db.Column(db.String())
    timestamp = db.Column(db.String(64))
