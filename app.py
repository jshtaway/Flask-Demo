import pandas as pd
import datetime as dt

from flask import (
    Flask,
    render_template,
    jsonify)


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///db/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print(Base.classes.keys())
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify('This is a simple REST API. Try these urls to get weather information:\
            \
            \
            /api/v1.0/precipitation\
                \
                /api/v1.0/stations\
                    \
                    /api/v1.0/tobs\
                        \
                /api/v1.0/<start>/<end>')


@app.route('/api/v1.0/precipitation')
def precipitation():
    dateList = [int(el) for el in max(session.query(
        Measurement.date).all()).date.split('-')]
    earliestDate = dt.date(*dateList) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs, Measurement.date).filter(
        Measurement.date > earliestDate)
    temperatures = {}
    for tobs, date in results:
        temperatures[str(date)] = str(tobs)
    return jsonify(temperatures)


@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    return(jsonify(results))


@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.tobs).all()
    return(jsonify(results))


@app.route('/api/v1.0/<start>/<end>')
def startEnd(start, end):
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    if not end:
        end = dt.datetime.today()  # .strftime("%Y-%m-%d")
    else:
        end = dt.datetime.strptime(end, "%Y-%m-%d")
    # print(end)
    results = session.query(Measurement.tobs).filter(
        Measurement.date > start).filter(Measurement.date < end).all()
    print(type(results[0]))
    resultsList = []
    [results.append(r[0]) for r in results]
    mintemp = min(results)
    maxtemp = max(results)
    avetemp = sum(results)/len(results)
    return(jsonify([mintemp, maxtemp, avetemp]))


if __name__ == '__main__':
    app.run(debug=True)
