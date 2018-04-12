# ## Step 4 - Climate App
# Now that you have completed your initial analysis, design a Flask api based on the queries that you have just developed.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt 
import time

import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy import create_engine, inspect, func
from sqlalchemy.orm import Session
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii_final.sqlite", echo = False)
inspector = inspect(engine)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect = True)
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# * Use FLASK to create your routes.
app = Flask(__name__)
# ### Routes

@app.route("/")
def welcome():
    print ("Working")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"---->example: /api/v1.0/2018-09-09/2018-09-17<br/>"
    )

# * `/api/v1.0/precipitation`
#   * Query for the dates and temperature observations from the last year.
@app.route("/api/v1.0/precipitation")
def precipitation():
    startdate = dt.datetime.today()
    yearAgo = startdate + dt.timedelta(days=-2*365)
    rain_list = []
    percipitation_query = session.query(Measurements.date, func.sum(Measurements.prcp))\
                        .filter(Measurements.date >= yearAgo)\
                        .group_by(Measurements.date).all()
    for rainy in percipitation_query:
        pdate = rainy[0].strftime("%Y-%m-%d")
        prain = round(rainy[1], 5)
        prcp_dict = {"date":pdate, "prcp":prain}
        rain_list.append(prcp_dict)
    return jsonify(rain_list)
#   * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

#   * Return the json representation of your dictionary.

# * `/api/v1.0/stations`
@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation).all()
    s_list = []
    for data in station_query:
        sID = data[0]
        sName = data[1]
        sLat = data[2]
        sLon = data[3]
        sEle = data[4]
        s_dict = {"station_id": sID,
                  "station_name": sName,
                  "station_latitude": sLat,
                  "station_longitude": sLon,
                  "station_elevation": sEle}
        s_list.append(s_dict)
    return jsonify(s_list)
#   * Return a json list of stations from the dataset.

# * `/api/v1.0/tobs`
@app.route("/api/v1.0/tobs")
def tobs():
    startdate = dt.datetime.today()
    yearAgo = startdate + dt.timedelta(days=-2*365)
    temp_list = []
    tobs_query = session.query(Measurements.date, func.avg(Measurements.tobs), func.min(Measurements.tobs), func.max(Measurements.tobs))\
                        .filter(Measurements.date >= yearAgo)\
                        .group_by(Measurements.date).all()
    for temp in tobs_query:
        tdate = temp[0].strftime("%Y-%m-%d")
        tavg = round(temp[1], 5)
        tmin = round(temp[2], 5)
        tmax = round(temp[3], 5)
        temp_dict = {"date":tdate, "temp_avg":tavg, "temp_max": tmax, "temp_min":tmin}
        temp_list.append(temp_dict)
    return jsonify(temp_list)
#   * Return a json list of Temperature Observations (tobs) for the previous year

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#   * Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# @app.route("/api/v1.0/<start_date>")
# def start(start_date):
#     try:
#         yearStart = int(start_date[0:4])
#         monthStart = int(start_date[5:7])
#         dayStart = int(start_date[8:])
#         startdate = dt.datetime(yearStart, monthStart, dayStart)
#         temp_list = []
#         tobs_query = session.query(Measurements.date, func.avg(Measurements.tobs), func.min(Measurements.tobs), func.max(Measurements.tobs))\
#                             .filter(Measurements.date >= startdate)\
#                             .group_by(Measurements.date).all()       
#         for temp in tobs_query:
#             tdate = temp[0].strftime("%Y-%m-%d")
#             tavg = round(temp[1], 5)
#             tmin = round(temp[2], 5)
#             tmax = round(temp[3], 5)
#             temp_dict = {"date":tdate, "temp_avg":tavg, "temp_max": tmax, "temp_min":tmin}
#             temp_list.append(temp_dict)
#         return jsonify(temp_list)
#     except:
#         return jsonify({"Error":"Please make sure that the date requested is in the following format: yyyy-mm-dd"})
@app.route("/api/v1.0/<start>/")
@app.route("/api/v1.0/<start>/<end>/")
def start_end(start=None, end=None):
    try:
        yearStart = int(start[0:4])
        monthStart = int(start[5:7])
        dayStart = int(start[8:])
        startdate = dt.datetime(yearStart, monthStart, dayStart)
        temp_list = []
        if end == None:
            enddate = None
            tobs_query = session.query(Measurements.date, func.avg(Measurements.tobs), func.min(Measurements.tobs), func.max(Measurements.tobs))\
                                .filter(Measurements.date >= startdate)\
                                .group_by(Measurements.date).all()
        else:
            yearEnd = int(end[0:4])
            monthEnd = int(end[5:7])
            dayEnd = int(end[8:])
            enddate = dt.datetime(yearEnd, monthEnd, dayEnd)
            tobs_query = session.query(Measurements.date, func.avg(Measurements.tobs), func.min(Measurements.tobs), func.max(Measurements.tobs))\
                                .filter(Measurements.date >= startdate).filter(Measurements.date <= enddate)\
                                .group_by(Measurements.date).all()            
        for temp in tobs_query:
            tdate = temp[0].strftime("%Y-%m-%d")
            tavg = round(temp[1], 5)
            tmin = round(temp[2], 5)
            tmax = round(temp[3], 5)
            temp_dict = {"date":tdate, "temp_avg":tavg, "temp_max": tmax, "temp_min":tmin}
            temp_list.append(temp_dict)
        return jsonify(temp_list)
    except:
        return jsonify({"Error":"Please make sure that the date requested is in the following format: yyyy-mm-dd"})
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
if __name__ == '__main__':
    app.run(debug=True)
# ## Hints

# * You will need to join the station and measurement tables for some of the analysis queries.
# * Use Flask `jsonify` to convert your api data into a valid json response object.
