import traci
import time
import pytz
import datetime
import pandas as pd


def getdatetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Karachi"))
    DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    return DATIME


sumoCmd = ["sumo-gui", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

packVehicleData = []

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    for i in range(0, len(vehicles)):
        # Collect required vehicle properties
        timestep = getdatetime()
        speed = round(traci.vehicle.getSpeed(vehicles[i]) * 3.6, 2)  # Speed in km/h
        x, y = traci.vehicle.getPosition(vehicles[i])
        xm, ym = traci.simulation.convertGeo(x, y)  # Latitude and longitude
        laneid = traci.vehicle.getLaneID(vehicles[i])
        posm = round(traci.vehicle.getDistance(vehicles[i]), 2)  # Vehicle position from start of the lane

        # Pack these properties into the vehList
        vehList = [timestep, vehicles[i], [x, y], [xm, ym], speed, laneid, posm]

        # Print the collected vehicle data
        print("Vehicle: ", vehicles[i], " at datetime: ", timestep)
        print("Vehicle Data:", vehList)

        # Append vehList to packVehicleData
        packVehicleData.append(vehList)

        # Perform other operations or controls as needed
        # ...

# After the simulation loop ends

traci.close()

# Generate Excel file for vehicle data
columnnames = ['timestep', 'vehid', 'coord', 'gpscoord', 'spd', 'lane', 'posm']
vehicle_dataset = pd.DataFrame(packVehicleData, columns=columnnames)
vehicle_dataset.to_excel("vehicle_data.xlsx", index=False)
time.sleep(5)
