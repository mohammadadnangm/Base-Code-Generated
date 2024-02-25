import pandas as pd
import numpy as np

# Load the selected vehicle data
vehicle_data = pd.read_csv('selected_vehicle_data.csv')

# Read the selected cell ID from the DataFrame
selected_cell_id = vehicle_data['cell_id'].unique()[0]

# Function to select the group leader
def select_group_leader(vehicle_data):
    # Reset the 'group_leader' column to False for all vehicles
    vehicle_data['group_leader'] = False

    # Initialize the maximum total value and the group leader ID
    max_total_value = -1
    group_leader_id = None

    # Iterate over all vehicles in the cell
    for index, row in vehicle_data.iterrows():
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

    # Now you can assign boolean values without any warning
    vehicle_data.loc[vehicle_data['vehicle_id'] == group_leader_id, 'group_leader'] = True

    print("Group Leader Cell ID: ", selected_cell_id)
    print("Number of vehicles in cell: ", len(vehicle_data))
    print("Group Leader ID: ", group_leader_id)

    # Save the modified DataFrame to a CSV file
    vehicle_data.to_csv('selected_vehicle_data.csv', index=False)

    # Save the leader information to a new file
    with open('leader_info.txt', 'w') as file:
        file.write(f"Group Leader Cell ID: {selected_cell_id}\n")
        file.write(f"Number of vehicles in cell: {len(vehicle_data)}\n")
        file.write(f"Group Leader ID: {group_leader_id}\n")

    return vehicle_data  # Return the modified DataFrame

# Call the function
select_group_leader(vehicle_data)