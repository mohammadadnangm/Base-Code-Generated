import pandas as pd
import numpy as np

# Load the selected vehicle data
vehicle_data = pd.read_csv('selected_vehicle_data.csv')

# Read the selected cell ID from the DataFrame
selected_cell_id = vehicle_data['cell_id'].unique()[0]

def calculate_direct_trust(vehicle_data, selected_cell_id):
    # Initialize a counter for the number of vehicles
    vehicle_count = 0

    # Iterate over each row in the DataFrame
    for index, row in vehicle_data.iterrows():
        try:
            # Extract the values of the relevant attributes
            acting_frequency = row['acting_frequency']
            transmission_power = row['transmission_power']
            traffic_rules_obeyed = row['traffic_rules_obeyed']

            # Define the weight factors for each component of the direct trust metric
            acting_frequency_weight = 0.3
            transmission_power_weight = 0.3
            traffic_rules_obeyed_weight = 0.4

            # Calculate the direct trust metric
            direct_trust = (acting_frequency_weight * acting_frequency +
                            transmission_power_weight * transmission_power +
                            traffic_rules_obeyed_weight * traffic_rules_obeyed)

            # Assign the calculated direct trust to the 'direct_trust' column of the current row
            vehicle_data.loc[index, 'direct_trust'] = direct_trust

            # Increment the vehicle counter
            vehicle_count += 1

        except KeyError:
            print(f"Required data for vehicle with ID {row['vehicle_id']} not found in the data.")

    # Save the updated DataFrame to the original CSV file
    vehicle_data.to_csv('selected_vehicle_data.csv', index=False)

    # Print the results
    print(f"Direct trust of {vehicle_count} vehicles from cell ID {selected_cell_id} is calculated and saved into data.")

    return vehicle_data

calculate_direct_trust(vehicle_data, selected_cell_id)