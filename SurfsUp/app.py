# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route('/')
def homepage():
    return (
        f'Welcome to the Climate App!:<br/>'
        f'Available routes:<br/>' 
        f'/api/v1.0/precipitation:<br/>'
        f'/api/v1.0/stations:<br/>' 
        f'/api/v1.0/tobs:<br/>' 
        f'/api/v1.0/<start>:<br/>' 
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # query the database to get precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-07-23').all()

    precipitation_data = {record.date: record.prcp for record in results}

    return jsonify(precipitation_data)



@app.route('/api/v1.0/stations')
def stations():
    # query the database to get all stations
    results = session.query(Station.station).all()

    # Extract station names into a list
    stations_list = [record.station for record in results]

    return jsonify(stations_list)


@app.route('/api/v1.0/tobs')
def tobs():
# Find the most active station (station with most observations in the last year)
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        filter(Measurement.date >= '2016-08-23').\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).\
        first()
    
    # Get temperature observations for the most active station in the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station ==most_active_station.station).\
        filter(Measurement.date >= '2016-08-23').all()

 # Extract temperature data
    temperatures = [record.tobs for record in results]

    return jsonify(temperatures)

@app.route('/api/v1.0/<start>')
def temp_start(start):
    #query the database for temperature data starting from the start date given 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        all()
    
    return jsonify({
        'min_temp': results[0][0],
        'avg_temp': results[0][1],
        'max_temp': results[0][2]
    })

@app.route('/api/v1.0/<start>/<end>')
def temperature_range(start, end):
    # query the database for temperature data between the start and end dates given
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start, end)).\
        all()

    return jsonify({
        'min_temp':results[0][0],
        'avg_temp': results[0][1],
        'max_temp': results[0][2]
    })

if __name__ == "__main__":
        app.run(debug=True)