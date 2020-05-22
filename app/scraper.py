import requests
from app import db
from .models import USState
from app import app
from datetime import datetime, timedelta
from pathlib import Path
import json
import csv
import pandas as pd
import time


def save_us_state_data():

    USState.query.delete()
    db.session.commit()

    us_states_url = "https://covidtracking.com/api/v1/states/daily.csv"

    resp = requests.get(us_states_url)

    print("time to sleep")
    time.sleep(5)

    if resp.status_code == 200:
        df = pd.read_csv(us_states_url)

        for date, state, positive, positive_increase in zip(df["date"], df["state"], df["positive"], df["positiveIncrease"]):

            if positive_increase == "nan":
                positive_increase = 0

            month = ""
            # print(date)
            date = str(date)
            if(date[4:6] == '01'):
                month = "Jan "
            elif(date[4:6] == '02'):
                month = "Feb "
            elif(date[4:6] == '03'):
                month = "Mar "
            elif(date[4:6] == '04'):
                month = "Apr "
            elif(date[4:6] == '05'):
                month = "May "
            elif(date[4:6] == '06'):
                month = "Jun "
            elif(date[4:6] == '07'):
                month = "Jul "
            elif(date[4:6] == '08'):
                month = "Aug "
            elif(date[4:6] == '09'):
                month = "Sep "
            elif(date[4:6] == '10'):
                month = "Oct "
            elif(date[4:6] == '11'):
                month = "Nov "
            elif(date[4:6] == '12'):
                month = "Dec "
            day = date[6:8]
            clean = month + day

            print(clean)

            print(date)
            print(state)
            print(positive_increase)
            print()

            with app.app_context():
                us_state_data = USState(date=date, clean_date=clean, state=state, positive=positive, positive_increase=int(positive_increase))
                db.session.add(us_state_data)
                db.session.commit()
