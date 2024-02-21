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


# Function to calculate total trust
def calculate_total_trust(vehicle_data, random_cell_id, beta=0.7):
    # Ensure beta is within the specified range
    if not 0.5 < beta < 1:
        raise ValueError("Beta must be between 0.5 and 1")


    # Read the updated data from the CSV file
    vehicle_data = pd.read_csv('vehicle_data.csv')

    # Filter the DataFrame to include only the vehicles in the specified cell
    vehicle_data = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Create a new column 'total_trust' and initialize it with NaN
    vehicle_data['total_trust'] = np.nan

    for index, row in vehicle_data.iterrows():
        # Get the direct and indirect trust for the vehicle
        direct_trust = row['direct_trust']
        indirect_trust = row['indirect_trust']

        # Calculate the total trust as the weighted sum of the direct and indirect trust
        total_trust = beta * direct_trust + (1 - beta) * indirect_trust

        # Assign the calculated total trust to the 'total_trust' column of the current row
        vehicle_data.at[index, 'total_trust'] = total_trust

    # Save the updated DataFrame to a CSV file
    vehicle_data.to_csv('vehicle_data.csv', index=False)

calculate_total_trust(vehicle_data, random_cell_id)


