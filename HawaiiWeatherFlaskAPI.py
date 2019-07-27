# import libraries
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, url_for
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome to <strong> Hawaii </strong> Weather API !!! <br><br>"
        f"Click any of the below available Routes:<br><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/precipitation'>Precipitation</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/stations'>Stations</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/tobs'>Temperature Observations</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start'>Start (In the URL replace start by a date; Ex: 20160101)</a><br>"
        f"<a href='http://127.0.0.1:5000/api/v1.0/start/end'>Start And End (In the URL replace start and end by dates. Ex:20160101) </a><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    date_prcp = session.query(Measure.date, Measure.prcp).all()
    date_prcp_dict = []

    for date, prcp in date_prcp:
        date_prcp_dict_s = {}
        date_prcp_dict_s["date"] = date
        date_prcp_dict_s["prcp"] = prcp
        date_prcp_dict.append(date_prcp_dict_s)    

    all_names = list(np.ravel(date_prcp_dict))
    return jsonify(all_names)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.name).all()
    all_names = list(np.ravel(station_results))
    return jsonify(all_names)

@app.route("/api/v1.0/tobs")    
def tobs():
    last_date = session.query(Measure.date).order_by(Measure.date.desc()).first()
    last_date_list = list(last_date)
    tobs = session.query(Measure.tobs).filter(func.strftime("%Y", Measure.date) == func.strftime("%Y", last_date_list[0])).all()    
    tobs_list = list(np.ravel(tobs))
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def tobs_onlystart(start):
    start_date_res = session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
                filter(Measure.date >= start).all()
    start_date_list = list(start_date_res)
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def tobs_startandend(start, end):
    start_end_date_res = session.query(func.min(Measure.tobs), func.avg(Measure.tobs), func.max(Measure.tobs)).\
                filter(Measure.date >= start).filter(Measure.date <= end).all()
    start_end_date_res_list = list(start_end_date_res)
    return jsonify(start_end_date_res_list)    

if __name__ == '__main__':
    app.run(debug=False)