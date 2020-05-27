import requests
from app import db
from .models import USState
from app import app
from datetime import datetime, timedelta
from pathlib import Path
import json
import csv
import pandas as pd


def split_dates(dates):
    """ 
    convert list or any kind iterable of dates to splitted dates with hyphen 

    input: list of date string like this ["20200423", "20210404"]

    return: list of dates i.e ["2020-04-23", "2021-10-04]
    """
    splitted_dates = []
    for date in dates:
        date = str(date)
        full_dates = f"{date[0:4]}-{date[4:6]}-{date[6:8]}"
        splitted_dates.append(full_dates)
    return splitted_dates


def get_clean_date(list_of_date_str):

    clean_dates = []
    for date in list_of_date_str:
        # convert date str to datetime object
        date_object = datetime.strptime(date, "%Y-%m-%d")
        # convert date object to date string like this 24 May 2020
        converted_date = date_object.strftime("%d %b")
        clean_dates.append(converted_date)
    return clean_dates


def download_us_state_data():
    us_states_url = "https://covidtracking.com/api/v1/states/daily.json"
    df = pd.read_json(us_states_url)

    splitted_dates = split_dates(df["date"])
    clean_date = get_clean_date(splitted_dates)
    df["date"] = clean_date

    selected_column = df[["date", "state", "positive", "positiveIncrease"]]

    selected_column.to_csv("us_state_data.csv")

    print("Us state data downloaded")


def download_all_countries_data():
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"

    df = pd.read_csv(url)

    # modify the date column to date like this '27 May'
    df["date"] = get_clean_date(df["date"])

    selected_column = df[["date", "iso_code", "location",
                          "total_cases", "new_cases", "total_deaths", "new_deaths"]]

    selected_column.to_csv("All_countries_data.csv")

    print("All countries data downloaded")


# download_us_state_data()
# download_all_countries_data()
