from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.forms import LocationForm
#from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import save_us_state_data


scheduler = BackgroundScheduler()
scheduler.add_job(func=save_us_state_data, trigger="interval", seconds=1800)
scheduler.start()


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():

    #form = LocationForm()
    data = []
    print("testingtestingbuttonsmash")
    from_location = ""
    to_location = ""
    # print(request.form['from-search-term'])

    return render_template('index.html', title='Teacher Home', start=from_location, end=to_location)


@app.route('/data', methods=['GET', 'POST'])
def data():

    print(request.form["from-search-term"])
    print(request.form["to-search-term"])

    test_data = ["Copper", 8.94, "#b87333"]

    print("this is the test data")
    print(test_data)

    from_location = request.form["from-search-term"]
    to_location = request.form["to-search-term"]

    return render_template('index.html', title='What', start=from_location, end=to_location, test=test_data)
