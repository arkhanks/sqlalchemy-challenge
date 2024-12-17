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
        "Welcome to the Climate App!:<br/>"
        "Available routes:<br/>" 
        "/api/v1.0/precipitation:<br/>"
        "/api/v1.0/stations:<br/>" 
        "/api/v1.0/tobs:<br/>" 
        "/api/v1.0/<start>:<br/>" 
        "/api/v1.0/<start>/<end>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # query the database to get precipitation data for the last 12 months
    query = "SELECT date, prcp FROM measurements WHERE date >= '2016-07-23'"
    result = connection.execute(query).all()

    precipitation_data = {record['date']: record['prcp'] for record in result}

    return jsonify(precipitation_data)


    if __name__ == "__main__":
        app.run(debug=True)