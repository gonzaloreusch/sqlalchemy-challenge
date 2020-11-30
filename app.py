#import dependencies
import numpy as np
import datetime as dt
from datetime import date
from datetime import timedelta
from flask import Flask, jsonify
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#engine to hawaii.sqlite db
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
base=automap_base()
# reflect the tables
base.prepare(engine, reflect=True)
# Save references to each table
Measurement=base.classes.measurement
Station=base.classes.station
#app
app=Flask(__name__)
#Flask routes
@app.route("/")
def home_page():
    """Travel climate research"""
    return(
        f"Available Routes:<br/>"
        f"Precipitation/api/v1.0/precipitation<br/>"
        f"Stations/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    lyq=date.fromisoformat(latest[0])-timedelta(365)
    Results=session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date>=lyq).all()
    session.close()
    precipita=[]
    for results in Results:
        r={}
        r[Result[0]]=Result[1]
        precipita.append(r)
    return jsonify(precipita)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    stations=session.query(Station.station).all()
    station_ls=np.ravel(stations).tolist()
    session.close()
    return jsonify(station_ls)    
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    lyq=date.fromisoformat(latest[0])-timedelta(365)
    actst=session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    statobs12mo=session.query(Measurement.tobs).filter(Measurement.station==actst[0][0]).\
    filter(Measurement.date>=lyq).all()
    statobs12mo_list=[tobs[0]for tobs in statobs12mo]
    session.close()
    return jsonify(statobs12mo_list) 

