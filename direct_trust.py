import pandas as pd
import numpy as np
import random
import math
import ast

# Assuming the vehicle_data DataFrame is already loaded
vehicle_data = pd.read_csv('vehicle_data.csv')

# Get a list of unique cell IDs
unique_cell_ids = vehicle_data['cell_id'].unique()

# Select a random cell ID
random_cell_id = random.choice(unique_cell_ids)


# Function to calculate direct trust
def calculate_direct_trust(vehicle_data, random_cell_id):
    # Read the data from the CSV file
    vehicle_data = pd.read_csv('vehicle_data.csv')

    # Filter the DataFrame to include only the vehicles in the specified cell
    vehicle_data = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Add a new column for direct trust
    vehicle_data['direct_trust'] = np.nan

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
            vehicle_data.at[index, 'direct_trust'] = direct_trust

        except KeyError:
            print(f"Required data for vehicle with ID {row['vehicle_id']} not found in the data.")

    # Save the updated DataFrame to a CSV file
    vehicle_data.to_csv('vehicle_data.csv', index=False)

    return vehicle_data

calculate_direct_trust(vehicle_data, random_cell_id)

