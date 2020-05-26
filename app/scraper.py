import requests
from app import db
from .models import USState, Countries
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

        csv_data=pd.DataFrame(columns=['date','clean_date','state','positive','positive_increase'])

        for date, state, positive, positive_increase in zip(df["date"], df["state"], df["positive"], df["positiveIncrease"].fillna(0)):

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

            tempdf=pd.DataFrame(date, clean, state, positive, int(positive_increase))
            csv_data.append(tempdf)
            print("this is the csv data")
            print(csv_data)

            with app.app_context():
                us_state_data = USState(date=date, clean_date=clean, state=state, positive=positive, positive_increase=int(positive_increase))
                db.session.add(us_state_data)
                db.session.commit()

    Countries.query.delete()
    db.session.commit()

    worldwide_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

    resp = requests.get(worldwide_url)

    if resp.status_code == 200:
        df = pd.read_csv(worldwide_url)

        for date, country, positive, positive_increase in zip(df["date"], df["location"], df["total_cases"], df["new_cases"].fillna(0)):

            if positive_increase == "nan":
                positive_increase = 0

            date = str(date)
            if(date[5:7] == '01'):
                month = "Jan "
            elif(date[5:7] == '02'):
                month = "Feb "
            elif(date[5:7] == '03'):
                month = "Mar "
            elif(date[5:7] == '04'):
                month = "Apr "
            elif(date[5:7] == '05'):
                month = "May "
            elif(date[5:7] == '06'):
                month = "Jun "
            elif(date[5:7] == '07'):
                month = "Jul "
            elif(date[5:7] == '08'):
                month = "Aug "
            elif(date[5:7] == '09'):
                month = "Sep "
            elif(date[5:7] == '10'):
                month = "Oct "
            elif(date[5:7] == '11'):
                month = "Nov "
            elif(date[5:7] == '12'):
                month = "Dec "
            day = date[8:10]
            clean = month + day

            print(date)
            print(clean)
            print(country)
            print(positive_increase)
            print()


            with app.app_context():
                country_data = Countries(date= date, clean_date=clean, country_code=country, cases=int(positive_increase))
                db.session.add(country_data)
                db.session.commit()
