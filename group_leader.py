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



# Function to select the group leader
def select_group_leader(random_cell_id):
    # Filter the DataFrame to only include vehicles in the randomly selected cell
    cell_vehicles = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Initialize the maximum total value and the group leader ID
    max_total_value = -1
    group_leader_id = None

    # Iterate over all vehicles in the cell
    for index, row in cell_vehicles.iterrows():
        # Calculate the centrality of the vehicle
        Centerness = 1 / row['distance'] if row['distance'] != 0 else float('inf')

        # Calculate the total value for the vehicle
        Total_trust = row['total_trust']
        Resources = row['resources']
        total_value = Total_trust + Centerness + Resources

        # Update the maximum total value and the group leader ID
        if total_value > max_total_value:
            max_total_value = total_value
            group_leader_id = row['vehicle_id']

    # Cast the 'group_leader' column to boolean type
    vehicle_data['group_leader'] = vehicle_data['group_leader'].astype(bool)

    # Now you can assign boolean values without any warning
    vehicle_data.loc[vehicle_data['cell_id'] == random_cell_id, 'group_leader'] = False
    vehicle_data.loc[vehicle_data['vehicle_id'] == group_leader_id, 'group_leader'] = True

    print("Group Leader Cell ID: ", random_cell_id)
    print("Group Leader ID: ", group_leader_id)

    return vehicle_data  # Return the modified DataFrame


# Call the function with the appropriate cell ID
select_group_leader(random_cell_id)




