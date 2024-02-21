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


# Function to calculate indirect trust
def calculate_indirect_trust(vehicle_data, random_cell_id):
    # Read the data from the CSV file
    vehicle_data = pd.read_csv('vehicle_data.csv')

    # Filter the DataFrame to include only the vehicles in the specified cell
    vehicle_data = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Add a new column for indirect trust
    vehicle_data['indirect_trust'] = np.nan

    for index, row in vehicle_data.iterrows():
        try:
            # Get the neighbors for the current vehicle based on the cell
            neighbors = get_neighbors_based_on_cell(row['vehicle_id'])  # Replace with your function to get neighbors

            # Extract relevant attributes for the neighbors
            neighbor_direct_trusts = vehicle_data[vehicle_data['vehicle_id'].isin(neighbors)]['direct_trust']

            # Calculate the indirect trust as the average of the neighbors' direct trusts
            indirect_trust = neighbor_direct_trusts.mean()

            # Assign the calculated indirect trust to the 'indirect_trust' column of the current row
            vehicle_data.at[index, 'indirect_trust'] = indirect_trust

        except KeyError:
            print(f"Required data for vehicle with ID {row['vehicle_id']} not found in the data.")

    # Save the updated DataFrame to a CSV file
    vehicle_data.to_csv('vehicle_data.csv', index=False)

# Function to get neighbors based on cell
def get_neighbors_based_on_cell(vehicle_id):
    # Get the cell ID for the vehicle
    cell_id = vehicle_data[vehicle_data['vehicle_id'] == vehicle_id]['cell_id'].values[0]

    # Get the list of vehicles in the same cell
    cell_vehicles = vehicle_data[vehicle_data['cell_id'] == cell_id]['vehicle_id'].values

    # Remove the current vehicle from the list
    cell_vehicles = cell_vehicles[cell_vehicles != vehicle_id]

    return cell_vehicles


calculate_indirect_trust(vehicle_data, random_cell_id)



