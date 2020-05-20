from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app.forms import LocationForm
#from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import save_us_state_data
from app.models import USState
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app)


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

    #THIS IS THE CODE FOR THE "FROM" SECTION
    from_location = request.form["from-search-term"]
    if len(from_location) > 0:
        search_from = "true"
    from_array = [x.strip() for x in from_location.split(',')]
    if from_array[(len(from_array) - 1)] == "USA":
        print("it's in the USA")
        state_code = from_array[(len(from_array) - 2)]
        #TO DO: MAKE A SEPERATE TABLE TO CROSS REFERENCE STATE CODES FOR FULL STATE NAMES
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

        last_seven_days_from = []
        last_seven_total_from = 0
        seven_before_total_from = 0
        for i in range(7):
            last_seven_days_from.append(stat_array_from[i])
            last_seven_total_from += int(stat_array_from[i])
            seven_before_total_from += int(stat_array_from[i + 7])


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

    return render_template('index.html', search_from=search_from, search_to=search_to, start=from_location, end=to_location, title="test chart", max=1000, values=stat_array_from, google_from=google_array_from, google_to=google_array_to, weekly_from=last_seven_comma_from, change_from=change_from, direction_from=direction_from, weekly_to=last_seven_comma_to, change_to=change_to, direction_to=direction_to )
