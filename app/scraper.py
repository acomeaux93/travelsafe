import requests
from app import db
from .models import USState
from app import app


def save_us_state_data():
    us_states_url = "https://covidtracking.com/api/v1/states/daily.json"

    resp = requests.get(us_states_url)
    if resp.status_code == 200:
        for data in resp.json():
            date = data.get("date")
            state = data.get("state")
            positive = data.get("positive")
            positive_increase = data.get("positiveIncrease")

            print(date)
            print(state)
            print(positive_increase)
            print()

            with app.app_context():
                us_state_data = USState(
                    date=date, state=state, positive=positive, positive_increase=positive_increase)
                db.session.add(us_state_data)
                db.session.commit()
