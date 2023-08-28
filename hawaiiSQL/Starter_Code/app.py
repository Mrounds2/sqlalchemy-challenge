# Import the dependencies.



#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################




#################################################
# Flask Routes
#################################################


from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

# Create an engine to connect to the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date (Enter date in yyyy-mm-dd format)<br/>"
        f"/api/v1.0/start_date/end_date (Enter dates in yyyy-mm-dd/yyyy-mm-dd format)"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
     # Create a new session
    session = Session(engine)
    # Calculate the date one year from the last date in data set
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query for precipitation data
    results = session.query(Measurement.date, Measurement.prcp).\
              filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    # Query for station data
    results = session.query(Station.station).all()

    # Convert the query results to a list
    station_list = [station[0] for station in results]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query for the most active station
    active_station = session.query(Measurement.station).\
                     group_by(Measurement.station).\
                     order_by(func.count(Measurement.station).desc()).first()[0]

    # Query for temperature observation data
    results = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.station == active_station).\
              filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary
    tobs_data = {date: tobs for date, tobs in results}

    # Close the session
    session.close()

    return jsonify(tobs_data)

# ... (additional code for start and start/end routes)

if __name__ == '__main__':
    app.run(debug=True, port=5001)