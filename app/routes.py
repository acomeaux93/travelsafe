from flask import render_template, flash, redirect, url_for, request, make_response
from datetime import datetime
from werkzeug.urls import url_parse
from app.forms import LocationForm, AlertForm
#from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import save_us_state_data
from app.models import USState, USReference, AlertRequests, LocationRequests
import os


if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=save_us_state_data, trigger="interval", seconds=60)
    scheduler.start()

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])

def index():

    #form = LocationForm()
    data = []
    print("testingtestingbuttonsmash")
    from_location = ""
    to_location = ""
    search_from = "false"
    search_to = "false"
    #print(request.form['from-search-term'])

    return render_template('index.html', search_from=search_from, search_to=search_to, title='Teacher Home', start=from_location, end=to_location)

@app.route('/data', methods=['GET', 'POST'])
def data():

    google_array_from = []
    google_array_to = []
    search_from = "false"
    search_to = "false"

    #Grab "From" and "To" info and save immediately to db
    from_for_db = request.form["from-search-term"]
    to_for_db = request.form["to-search-term"]
    search_time = datetime.now(tz=None)
    alert_log = LocationRequests(from_location=from_for_db, to_location=to_for_db, timestamp=search_time)
    db.session.add(alert_log)
    db.session.commit()

    #THIS IS THE CODE FOR THE "FROM" SECTION

    #Pulls From value from form and parses
    from_location = request.form["from-search-term"]
    if len(from_location) > 0:
        search_from = "true"
    from_array = [x.strip() for x in from_location.split(',')]

    #Checks Country designation of FROM. should replace this method with a search through the country database
    if from_array[(len(from_array) - 1)] == "USA":
        print("it's in the USA")
        state_code = from_array[(len(from_array) - 2)]
        state_reference = USReference.query.filter_by(state_abbreviation=state_code).first()
        country_name_from = from_array[(len(from_array) - 1)]
        region_name_from = state_reference.full_state_name
        population_from = state_reference.state_population
        population_from_clean = "{:,}".format(population_from)



        #References the databse to pull 30-day information for graph
        state_stats = USState.query.filter_by(state=state_code).limit(30).all()
        stat_array_from = []
        for value in state_stats:
            stat_array_from.append(value.positive_increase)
            google_ind = []
            google_ind.append(value.clean_date)
            google_ind.append(int(value.positive_increase))
            google_ind.append("blue")
            google_array_from.append(google_ind)

        google_array_from.reverse()

        print("this is the stat array")
        print(stat_array_from)

        #Cleans data for processing for descriptive statistics
        #Removes any zero entries from the database so that they are not included in the final calculation
        stat_array_from_clean = []
        for value in stat_array_from:
            if int(value) > 0:
                stat_array_from_clean.append(value)

        last_seven_days_from = []
        last_seven_total_from = 0
        seven_before_total_from = 0
        for i in range(7):
            last_seven_days_from.append(stat_array_from_clean[i])
            last_seven_total_from += int(stat_array_from_clean[i])
            seven_before_total_from += int(stat_array_from_clean[i + 7])


        #computing the daily average from the last seven Days
        seven_average = (last_seven_total_from / 7)
        pop_denominator = (population_from / 1000)
        per_1000_result_from = round((seven_average/pop_denominator), 3)
        print("This is the daily new infections per 1000 residents")
        print(per_1000_result_from)

        print("this is the last 7 days")
        print(last_seven_days_from)
        print("this is the 7 day total")
        print(last_seven_total_from)
        print("this is the 7 day total before that")
        print(seven_before_total_from)

        week_difference_from = last_seven_total_from/seven_before_total_from
        direction_from = ""
        if week_difference_from < 1.0:
            change_from = round(((1 - week_difference_from) * 100), 1)
            direction_from = " decrease"
        else:
            change_from = round(((week_difference_from - 1) * 100), 1)
            direction_from = " increase"

        print("This is the percentage change")
        print(str(change_from) + direction_from)

        last_seven_comma_from = "{:,}".format(last_seven_total_from)

    else:
        print("not in the USA")

    #THIS IS THE CODE FOR THE "TO" SECTION
    to_location = request.form["to-search-term"]
    if len(to_location) > 0:
        search_to = "true"
    to_array = [x.strip() for x in to_location.split(',')]
    if to_array[(len(to_array) - 1)] == "USA":
        print("it's in the USA")
        state_code = to_array[(len(to_array) - 2)]
        state_stats = USState.query.filter_by(state=state_code).limit(30).all()
        stat_array_to = []
        for value in state_stats:
            stat_array_to.append(value.positive_increase)
            google_ind = []
            google_ind.append(value.clean_date)
            google_ind.append(int(value.positive_increase))
            google_ind.append("blue")
            google_array_to.append(google_ind)

        google_array_to.reverse()

        print("this is the stat array")
        print(stat_array_to)

        last_seven_days_to = []
        last_seven_total_to = 0
        seven_before_total_to = 0
        for i in range(7):
            last_seven_days_to.append(stat_array_to[i])
            last_seven_total_to += int(stat_array_to[i])
            seven_before_total_to += int(stat_array_to[i + 7])


        print("this is the last 7 days")
        print(last_seven_days_to)
        print("this is the 7 day total")
        print(last_seven_total_to)
        print("this is the 7 day total before that")
        print(seven_before_total_to)

        week_difference_to = last_seven_total_to/seven_before_total_to
        direction_to = ""
        if week_difference_to < 1.0:
            change_to = round(((1 - week_difference_to) * 100), 1)
            direction_to = " decrease"
        else:
            change_to = round(((week_difference_to - 1) * 100), 1)
            direction_to = " increase"

        print("This is the percentage change")
        print(str(change_to) + direction_to)

        last_seven_comma_to = "{:,}".format(last_seven_total_to)

    else:
        print("not in the USA")

    print("this is google array from")
    print(google_array_from)
    print("this is google array to")
    print(google_array_to)


    #Cookies experimenting
    resp = make_response(render_template('index.html', region_name_from=region_name_from, pop_from=population_from_clean, per_1000_from=per_1000_result_from, country_name_from=country_name_from, search_from=search_from, search_to=search_to, start=from_location, end=to_location, title="test chart", max=1000, values=stat_array_from, google_from=google_array_from, google_to=google_array_to, weekly_from=last_seven_comma_from, change_from=change_from, direction_from=direction_from, weekly_to=last_seven_comma_to, change_to=change_to, direction_to=direction_to ))

    resp.set_cookie("flavor", "fudge")

    return resp

    # return render_template('index.html', res=res, region_name_from=region_name_from, pop_from=population_from_clean, per_1000_from=per_1000_result_from, country_name_from=country_name_from, search_from=search_from, search_to=search_to, start=from_location, end=to_location, title="test chart", max=1000, values=stat_array_from, google_from=google_array_from, google_to=google_array_to, weekly_from=last_seven_comma_from, change_from=change_from, direction_from=direction_from, weekly_to=last_seven_comma_to, change_to=change_to, direction_to=direction_to )


@app.route('/alerts', methods=['GET', 'POST'])
def alerts():
    form = AlertForm()

    if request.method == 'POST':
        flash("Alert Settings Recorded")
        test = form.daily_input.data
        location = request.form["location"]
        search_time = datetime.now(tz=None)
        print(test)
        print("This is all the form data")
        print(form.data)
        alert_log = AlertRequests(alert_location=location, form_data=str(form.data), timestamp=search_time)
        db.session.add(alert_log)
        db.session.commit()

        print(location)

    return render_template('alerts.html', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():

    return render_template('contact.html')
