import requests
from app import db
from .models import USState
from app import app
from datetime import datetime, timedelta
from pathlib import Path
import json
import csv
import pandas as pd


def download_us_state_data():
    us_states_url = "https://covidtracking.com/api/v1/states/daily.json"
    df = pd.read_json(us_states_url)

    clean_date = get_clean_date(list(df["date"]))
    df["date"] = clean_date

    selected_column = df[["date", "state", "positive", "positiveIncrease"]]

    selected_column.to_csv("custom_data.csv")

    print("Us state data downloaded")


def download_all_countries_data():
    url = "https://thevirustracker.com/timeline/map-data.json"

    try:
        resp = requests.get(url, stream=True)
        with open("all_countries_data.json", "wb") as file:
            file.write(resp.content)
        with open('all_countries_data.json') as json_data:
            data = json.load(json_data).get("data")
        df = pd.DataFrame.from_dict(data)
        print(len(df["countrycode"]))
        df["country_name"] = convert_iso_to_country_name(df["countrycode"])
        selected_column = df[["date", "countrycode", "country_name", "cases",
                              "death", "recovered"]]

        selected_column.to_csv("All_countries_data.csv")

        print("All countries data downloaded")
    except requests.ConnectionError as e:
        print(e)


def get_clean_date(list_of_dates):
    """ convert date like this 20200525 to May 25 """
    clean_dates = []
    for date in list_of_dates:
        month = ""
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

        clean_dates.append(clean)
        # print()
    return clean_dates


def save_us_state_data():

    USState.query.delete()
    db.session.commit()

    us_states_url = "https://covidtracking.com/api/v1/states/daily.csv"

    resp = requests.get(us_states_url)
    if resp.status_code == 200:
        df = pd.read_csv(us_states_url)

        for date, state, positive, positive_increase in zip(df["date"], df["state"], df["positive"], df["positiveIncrease"]):
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
            # print()

            with app.app_context():
                us_state_data = USState(
                    date=date, clean_date=clean, state=state, positive=positive, positive_increase=positive_increase)
                db.session.add(us_state_data)
                db.session.commit()


def save_all_countries_data():

    url = "https://thevirustracker.com/timeline/map-data.json"
    resp = requests.get(url)

    if resp.status_code == 200:
        data = resp.json().get("data")
        date = data.get("date")
        country_code = data.get("state")
        country_name = convert_iso_to_country_name(country_code)
        positive = data.get("cases")
        deaths = data.get("deaths")
        recovered = data.get("recovered")
        positive_increase = data.get("positiveIncrease")

        with app.app_context():
            Countries.query.delete()
            countries_data = Countries(
                date=date, country_code=country_code, country_name=country_name, positive_increase=positive_increase)
            db.session.add(countries_data)
            db.session.commit()


def convert_iso_to_country_name(list_of_contry_codes):
    """ Takes in country codes(ISO) as list and return country names as list """

    country_names = []
    data = Path("country_names_and_iso.json").read_text()
    countries_and_iso = json.loads(data)

    for iso_code in list_of_contry_codes:
        for country in countries_and_iso:
            if country.get("Code") == iso_code:
                country_names.append(country.get("Name"))
                break
    print(f"length of country names: {len(country_names)}")
    return country_names


download_us_state_data()
# download_all_countries_data()
