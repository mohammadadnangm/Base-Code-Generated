import pandas as pd
import numpy as np


# Load the selected vehicle data
vehicle_data = pd.read_csv('selected_vehicle_data.csv')

# Read the selected cell ID from the DataFrame
selected_cell_id = vehicle_data['cell_id'].unique()[0]

def calculate_indirect_trust(vehicle_data, selected_cell_id):
    # Initialize a counter for the number of vehicles
    vehicle_count = 0

    for index, row in vehicle_data.iterrows():
        # Check if the vehicle is in the selected cell
        if row['cell_id'] == selected_cell_id:
            try:
                # Get the neighbors for the current vehicle based on the cell
                neighbors = get_neighbors_based_on_cell(row['vehicle_id'])  # Replace with your function to get neighbors

                # Extract relevant attributes for the neighbors
                neighbor_direct_trusts = vehicle_data[vehicle_data['vehicle_id'].isin(neighbors)]['direct_trust']

                # Calculate the indirect trust as the average of the neighbors' direct trusts
                indirect_trust = neighbor_direct_trusts.mean()

            except KeyError:
                print(f"Required data for vehicle with ID {row['vehicle_id']} not found in the data.")
                # Set a default value for the indirect trust
                indirect_trust = 0

            # Assign the calculated indirect trust to the 'indirect_trust' column of the current row
            vehicle_data.loc[index, 'indirect_trust'] = indirect_trust

            # Increment the vehicle counter
            vehicle_count += 1

    # Save the updated DataFrame to a CSV file
    vehicle_data.to_csv('selected_vehicle_data.csv', index=False)

    # Print the results
    print(f"Indirect trust of {vehicle_count} vehicles from cell ID {selected_cell_id} is calculated and saved into data.")

    return vehicle_data

# Function to get neighbors based on cell
def get_neighbors_based_on_cell(vehicle_id):
    # Get the cell ID for the vehicle
    cell_id = vehicle_data[vehicle_data['vehicle_id'] == vehicle_id]['cell_id'].values[0]

    # Get the list of vehicles in the same cell
    cell_vehicles = vehicle_data[vehicle_data['cell_id'] == cell_id]['vehicle_id'].values

    # Remove the current vehicle from the list
    cell_vehicles = cell_vehicles[cell_vehicles != vehicle_id]

    return cell_vehicles

calculate_indirect_trust(vehicle_data, selected_cell_id)


