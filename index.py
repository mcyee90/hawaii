import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pymysql
pymysql.install_as_MySQLdb()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Float

from sqlalchemy import create_engine, inspect
engine = create_engine("sqlite:///hawaii_final.sqlite", echo = False)
inspector = inspect(engine)

from sqlalchemy.orm import Session
session = Session(engine)
from sqlalchemy import func

import datetime as dt 
import time

Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# ## Step 4 - Climate App
from flask import Flask, jsonify
# Now that you have completed your initial analysis, design a Flask api based on the queries that you have just developed.

# * Use FLASK to create your routes.
app = Flask(__name__)
# ### Routes

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precepitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>/<end><br/>"
    )
# * `/api/v1.0/precipitation`
#   * Query for the dates and temperature observations from the last year.
# @app.route("/api/v1.0/precipitation")
# def precipitation():
#     startdate = dt.datetime.today()
#     yearAgo = startdate + dt.timedelta(days=-2*365)
#     rain_list = []
#     percipitation_query = session.query(Measurements.date, func.sum(Measurements.prcp))\
#                         .filter(Measurements.date >= yearAgo)\
#                         .group_by(Measurements.date).all()
#     for rainy in percipitation_query:
#         pdate = rainy[0].strftime("%Y-%m-%d")
#         prain = round(rainy[1], 5)
#         prcp_dict = {"date":pdate, "prcp":prain}
#         rain_list.append(prcp_dict)
#     return jsonify(rain_list)
#   * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.

#   * Return the json representation of your dictionary.

# * `/api/v1.0/stations`
# @app.route("/api/v1.0/stations")
# def stations():
#     station_query = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation).all()
#     s_list = []
#     for data in station_query:
#         sID = data[0]
#         sName = data[1]
#         sLat = data[2]
#         sLon = data[3]
#         sEle = data[4]
#         s_dict = {"station_id": sID,
#                   "station_name": sName,
#                   "station_latitude": sLat,
#                   "station_longitude": sLon,
#                   "station_elevation": sEle}
#         s_list.append(s_dict)
#         return jsonify(s_list)
#   * Return a json list of stations from the dataset.

# * `/api/v1.0/tobs`

#   * Return a json list of Temperature Observations (tobs) for the previous year

# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

#   * Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

# ## Hints

# * You will need to join the station and measurement tables for some of the analysis queries.

# * Use Flask `jsonify` to convert your api data into a valid json response object.
