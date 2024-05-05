import os
import orhelper
from orhelper import FlightDataType, FlightEvent
from math import sqrt
import numpy as np

# Set the JAVA_HOME environment variable
os.environ['JAVA_HOME'] = 'JVM'

def cost(filename):
    dat = simFlight(filename)
    score = 0
    for i in range(2):
        score += (dat[i][3][0]>=0.1)*sqrt(2*(dat[i][0]*3.28084)**2/dat[i][1]/dat[i][2])/(dat[i][3][1]+0.88)
    return score


def simFlight(filename):
    # Use ORHelper to interact with OpenRocket
    flightData = []
    airframe_Length = 0.829
    with orhelper.OpenRocketInstance() as instance:
        orh = orhelper.Helper(instance)
        for i in range(2):
            # Load the OpenRocket document, run the simulation, and get data and events
            doc = orh.load_doc(os.path.join('.ork', filename))
            sim = doc.getSimulation(i)
            orh.run_simulation(sim)
            
            # Extract time series data for altitude and velocity
            data = orh.get_timeseries(sim, [FlightDataType.TYPE_TIME, FlightDataType.TYPE_ALTITUDE, FlightDataType.TYPE_VELOCITY_Z, FlightDataType.TYPE_CG_LOCATION, FlightDataType.TYPE_CP_LOCATION, FlightDataType.TYPE_REFERENCE_LENGTH])
            events = orh.get_events(sim)

            # Extract apogee and the time to apogee
            apogee_time = events[FlightEvent.APOGEE][0]  # Assumes the first occurrence is the primary one
            apogee_index = (data[FlightDataType.TYPE_TIME] == apogee_time).argmax()
            burnout_time = events[FlightEvent.BURNOUT][0]
            burnout_index = (data[FlightDataType.TYPE_TIME] == burnout_time).argmax()
            apogee_altitude = data[FlightDataType.TYPE_ALTITUDE][apogee_index]


            # Extract total flight duration
            # Assuming the last time recorded is the end of the flight
            total_flight_time = events[FlightEvent.GROUND_HIT][0] - events[FlightEvent.LIFTOFF][0]
            
            cg = data[FlightDataType.TYPE_CG_LOCATION][1]  # Last value, assuming stable throughout or at end of simulation
            cp_mean = np.nanmean(data[FlightDataType.TYPE_CP_LOCATION][0:apogee_index])
            cp_min = np.nanmin(data[FlightDataType.TYPE_CP_LOCATION][0:burnout_index])
            airframe_diam = data[FlightDataType.TYPE_REFERENCE_LENGTH]
            stability_percentage = [(cp_min-cg)/airframe_Length, (cp_mean-cg)/airframe_Length]

            flightData.append([apogee_altitude, apogee_time, total_flight_time, stability_percentage])

    return flightData


print(cost("sample.ork"))

