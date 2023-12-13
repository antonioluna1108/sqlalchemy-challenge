# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect = True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# Create all available routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return(f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        )

# Create Precipitation route that returns json with the date as the key and the value as the precipitation and Only returns the jsonified precipitation data for the last year in the database
@app.route("/api/v1.0/precipitation")
def precipitation():

# Create our session (link) from Python to the DB
    session = Session(engine) 

# Create new variable to store results from query to Measurement table for prcp and date columns
    precipitation_results = session.query(measurement.prcp, measurement.date).all()

# Close session
    session.close()

# Create a dictionary from the row data and append to a list of precipitation results
    precip_values = []
    for prcp, date in precipitation_results:
        precip_dict = {}
        precip_dict["precipitation"] = prcp
        precip_dict["date"] = date
        precipitation_results.append(precip_dict)

    return jsonify(precip_values)

# Create a route for stations
@app.route("/api/v1.0/stations")
def station():

# Create our session (link) from Python to the DB
    session = Session(engine) 

# Create new variable to store results from stations
    station_results = session.query(station.station, station.id).all()

    session.close()

# Create a dictionary from the row data and append to a list of station results
    station_values = []
    for stat, id in station_results:
        station_values_dict = {}
        station_values_dict['station'] = stat
        station_values_dict['id'] = id
        station_values.append(station_values_dict)

    return jsonify (station_values)

# Create a route for TOBS for most active station (USC00519281)
@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine) 

# Create a query of TOBS for the most active station for last years data from database
    last_year_data_results = session.query(measurement.date).\
        order_by(measurement.date.desc()).first()
   
    

# Create a directory from the data and append to a list of last year's results
    last_year_data_values = []
    for date in last_year_data_results:
        last_year_data_dict = {}
        last_year_data_dict["date"] = date
        last_year_data_values.append(last_year_data_dict)

# Create a query to find most active station
    active_station= session.query(measurement.station, func.count(measurement.station)).\
        order_by(func.count(measurement.station).desc()).\
        group_by(measurement.station).first()
    most_active_station = active_station[0] 
    most_active_station
    session.close()

# Create a directory of dates, TOBS, and stations that will append
    date_tobs_last_year_values =[]
    for date, tobs, stat in  date_tobs_last_year_values:
        date_tobs_last_year_dict = {}
        date_tobs_last_year_dict["date"] = date
        date_tobs_last_year_dict["tobs"] = tobs
        date_tobs_last_year_dict["station"] = stat
        date_tobs_last_year_values.append(date_tobs_last_year_dict)
    
    return jsonify(date_tobs_last_year_values)

# Create a start date route
@app.route("/api/v1.0/start")
def start_date(start):
    session = Session(engine) 


    # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
    start_date_tobs_results = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    session.close() 

# Create a list of min, max, avg that will append to the directory
    start_date_tobs_values = []
    for min, max, avg in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["TMIN"] = min
        start_date_tobs_dict["TMAX"] = max
        start_date_tobs_dict["TAVG"] = avg
        start_date_tobs_values.append(start_date_tobs_dict)

    return jsonify(start_date_tobs_values)

# Create a route for start date and end date
@app.route("api/v1.0/start/end")

# Create our session (link) from Python to the DB
def Start_date_end_date(start, end):
    session = Session(engine)
    
# Create query for min, max, and avg tobs where date is greater than or equal to start date and less then or equal to end date
    start_date_end_date_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    session.close()

# Create directory of min, max, and avg temps that will append
    start_date_end_date_values = []
    for min, max, avg in start_date_end_date_results:
        start_date_end_date_dict = {}
        start_date_end_date_dict["min"] = min
        start_date_end_date_dict["max"] = max
        start_date_end_date_dict["avg"] = avg
        start_date_end_date_values.append(start_date_end_date_dict)
    
    return jsonify(start_date_end_date_values)

if __name__ == '__main__':
    app.run(debug= True)








