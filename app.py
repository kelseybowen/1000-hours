from flask import Flask
from SQLiteClient import SQLiteClient
from Calendar import Calendar
from datetime import datetime, date

app = Flask(__name__)

database = "/Users/kbowen/PycharmProjects/1000-hours/1000hoursdev.db"
db = SQLiteClient(database)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<user>')
def status_page(user):
    cal = Calendar(user, database)
    return cal.render_json()

@app.route('/<user>/<year>-<month>-<day>')
def day_route(user, year, month, day):
    cal = Calendar(user, database)
    day_of_year = date(int(year), int(month), int(day))
    day_number = cal.date_list[int(day_of_year.strftime("%j"))-1]
    return str(day_number)

# TODO: GET STATUS

# TODO: ADD/UPDATE LOG

# TODO: VIEW SINGLE DAY LOG OR RANGE

# TODO: UPDATE GOAL

# TODO: DELETE HOUR LOG

#

