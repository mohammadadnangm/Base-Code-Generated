import pandas as pd
import numpy as np


# Load the selected vehicle data
vehicle_data = pd.read_csv('selected_vehicle_data.csv')

# Read the selected cell ID from the DataFrame
selected_cell_id = vehicle_data['cell_id'].unique()[0]


def calculate_total_trust(vehicle_data, selected_cell_id, beta=0.7):
    # Ensure beta is within the specified range
    if not 0.5 < beta < 1:
        raise ValueError("Beta must be between 0.5 and 1")

    # Initialize a counter for the number of vehicles
    vehicle_count = 0

    for index, row in vehicle_data.iterrows():
        # Only calculate total trust for rows that have non-null direct and indirect trust values
        # and are in the selected cell
        if row['cell_id'] == selected_cell_id and pd.notnull(row['direct_trust']) and pd.notnull(row['indirect_trust']):
            # Get the direct and indirect trust for the vehicle
            direct_trust = row['direct_trust']
            indirect_trust = row['indirect_trust']

            # Calculate the total trust as the weighted sum of the direct and indirect trust
            total_trust = beta * direct_trust + (1 - beta) * indirect_trust

            # Assign the calculated total trust to the 'total_trust' column of the current row
            vehicle_data.loc[index, 'total_trust'] = total_trust

            # Increment the vehicle counter
            vehicle_count += 1

    # Save the updated DataFrame to a CSV file
    vehicle_data.to_csv('selected_vehicle_data.csv', index=False)

    # Print the results
    print(f"Total trust of {vehicle_count} vehicles from cell ID {selected_cell_id} is calculated and saved into data.")

    return vehicle_data

calculate_total_trust(vehicle_data, selected_cell_id)
