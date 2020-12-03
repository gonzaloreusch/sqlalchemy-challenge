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
#conn=engine.connect()
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
    return(
        f"Travel climate research<br/><br/>"+
        f"Available Routes:<br/><br/>"+
        f"Precipitation/api/v1.0/precipitation<br/>"+
        f"Stations/api/v1.0/stations<br/>"+
        f"/api/v1.0/tobs<br/><br/>"+
        f"/api/v1.0/start/<start>"+
        f" (Note: Enter start date after'/' in YYYY-MM-DD format.) <br/> <br/>"+  #Thanks Gary!!
        f"/api/v1.0/date_range/<start>/<end> "+
        f"   (Note: Enter date range format: start date/end date (i.e. YYYY-MM-DD/YYYY-MM-DD))<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    latest=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lyq=date.fromisoformat(latest[0])-timedelta(365)
    Results=session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date>=lyq).all()
    session.close()
    precipita=[]
    for result in Results:
        r={}
        r[result[0]]=result[1]
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
    latest=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lyq=date.fromisoformat(latest[0])-timedelta(365)
    actst=session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    statobs12mo=session.query(Measurement.tobs).filter(Measurement.station==actst[0][0]).\
    filter(Measurement.date>=lyq).all()
    statobs12mo_list=[tobs[0]for tobs in statobs12mo]
    session.close()
    return jsonify(statobs12mo_list) 

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session = Session(engine)
    calc_results = session.query(func.min(Measurement.tobs),\
                    func.avg(Measurement.tobs),\
                    func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    session.close()
    valor1 = list(np.ravel(calc_results))
    Temps = {"Start Date": start,
             "TMIN": valor1[0],
             "TAVG": valor1[1],
             "TMAX": valor1[2]}
    return jsonify(Temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    session = Session(engine)  
    results = session.query(func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs)).\
                            filter(Measurement.date >= start).\
                            filter(Measurement.date <= end).all()

    session.close()
    values = list(np.ravel(results))
    Temps = {"Start Date": start,
                "End Date": end,
                "TMIN": values[0],
                "TAVG": values[1],
                "TMAX": values[2]}
    return jsonify(Temps)
if __name__ == '__main__':
    app.run(debug=True)
    