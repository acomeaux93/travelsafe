import requests
from app import db
from .models import USState
from app import app


def save_us_state_data():
    us_states_url = "https://covidtracking.com/api/v1/states/daily.json"

    USState.query.delete()
    db.session.commit()

    resp = ""
    resp = requests.get(us_states_url)
    print(resp.json())
    if resp.status_code == 200:
        for data in resp.json():
            date = str(data.get("date"))
            #print(date[4:6])
            month = ""
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
            #print(clean)

            state = data.get("state")
            positive = data.get("positive")
            positive_increase = data.get("positiveIncrease")

            # print(date)
            # print(state)
            # print(positive_increase)
            # print()

            # with app.app_context():
            #     us_state_data = USState(
            #         date=date, clean_date=clean, state=state, positive=positive, positive_increase=positive_increase)
            #     db.session.add(us_state_data)
            #     db.session.commit()
