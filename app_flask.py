from logging import StringTemplateStyle
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, time

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, query
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():

    """List all available api routes."""
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last year of Precipitation Data"""
    session = Session(engine)

    """Return a list of the dates and precipitation from last year"""
    # Query for the dates and precipitation from last year
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date


    #convert last date string to date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")

    #calculate date one year after last date using timedelta datetime function
    first_date = last_date - dt(days=365)

    #perform a query to retreive the data and precipitation scores
    last_year_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= first_date).all()
    return jsonify(last_year_data)


@app.route("/api/v1.0/passengers")
def stations():

    """List of Weather stations"""

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # select station names from stations table
    stations = session.query(Station.station).all()

    # Return JSONIFY List of Stations

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Temperature observartion for Top Station for last year"""

    session = Session(engine)

    #find last date in database from Measurements
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    #convert last date string to date
    last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")

    #calculate date one year after last date using timedelta datetime function
    first_date = last_date - dt(days=365)

    #list the stations and the counts in descending order
    station_counts = session.query(Measurement.station, func.count(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc().all()

    #create top station variable from tuple
    top_station = (station_counts[0])
    top_station = (top_station[0])

    #calculate the lowest temperature and the highest temperature recorded, and averge temperature of the most active station.
    session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.station == top_station).all()

    #query the last 12 months of tempearture observation data for this station and plot the results as a histogram
    filter(Measurement.station == top_station).filter(Measurement.date >= first_date).all()
    return jsonify(top_station_year_obs)

@app.route("/api/v1/0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)

    """Return Temperature Min, Temperature Avg, Temperature Max"""

    #select statement
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        #calculate Temperature Min, Temperature Avg, Temperature Max for dates greater than start
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        #Ravel results into a 1D array and convert to a list
        temps = list(np.ravel(results))
        return jsonify(temps)

        #calculate Temperature Min, Temperature Avg, Temperature Max with start and stop
        results = session.query(*sel).\
            filter(Mesurement.date >= start).\
            filter(Measurement.date <= end),all()
        return jsonify(results)

    if __name__ == '__main__':
        app.run()