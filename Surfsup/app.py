# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


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
app = Flask(__name__)
# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
def home():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query for the date and precipitation for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()
    
    session.close

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all stations
    results = session.query(Station.station).all()
    
    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

('USC00519281', 2772)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    # Convert the query results to a list
    temp_data = list(np.ravel(results))

    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start-end range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    # Convert the query results to a list
    temp_data = list(np.ravel(results))

    return jsonify(temp_data)



if __name__ == '__main__':
    app.run(debug=True)

