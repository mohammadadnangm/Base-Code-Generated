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


    return vehicle_data





# Function to calculate indirect trust
def calculate_indirect_trust(vehicle_data, random_cell_id):

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







# Function to calculate total trust
def calculate_total_trust(vehicle_data, random_cell_id, beta=0.7):
    # Ensure beta is within the specified range
    if not 0.5 < beta < 1:
        raise ValueError("Beta must be between 0.5 and 1")


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

    return vehicle_data





# Function to calculate distance from the cell center
def calculate_distance(vehicle_data, random_cell_id, cell_size):
    # Get the cell center and radius for the random cell ID
    cell_center, cell_radius = get_cell_data(random_cell_id, cell_size)

    # Filter the DataFrame to only include vehicles in the randomly selected cell
    cell_vehicles = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Iterate over all vehicles in the cell
    for index, row in cell_vehicles.iterrows():
        # Calculate the Euclidean distance between the vehicle and the cell center
        raw_distance = math.sqrt((row['longitude'] - cell_center[0])**2 + (row['latitude'] - cell_center[1])**2)

        # Subtract the cell radius from the calculated distance
        distance = raw_distance - cell_radius

        # Save the calculated distance in the DataFrame
        vehicle_data.loc[index, 'distance'] = distance


    return vehicle_data


# Function to calculate cell data
def get_cell_data(cell_id, cell_size):
    # Convert the cell ID back to a tuple
    cell_id = ast.literal_eval(cell_id)

    # Calculate the cell center
    cell_center_x = (float(cell_id[0]) * cell_size) + (cell_size / 2)
    cell_center_y = (float(cell_id[1]) * cell_size) + (cell_size / 2)
    cell_center = (cell_center_x, cell_center_y)

    # Calculate the cell radius
    cell_radius = cell_size / 2

    return cell_center, cell_radius



# Function to evaluate resources
def evaluate_resources(vehicle_data, random_cell_id):
    # Get the rows for the vehicles in the random cell from the DataFrame
    vehicle_rows = vehicle_data[vehicle_data['cell_id'] == random_cell_id]

    # Define the weight factors for each component of the resources evaluation
    processing_power_weight = 0.5
    available_storage_weight = 0.5

    # Iterate over each vehicle in the cell
    for index, vehicle_row in vehicle_rows.iterrows():
        # Get the processing power and available storage for the vehicle from the DataFrame
        processing_power = vehicle_row['processing_power']
        available_storage = vehicle_row['available_storage']

        # Calculate the resources evaluation
        resources = (processing_power_weight * processing_power +
                     available_storage_weight * available_storage)

        # Save the calculated resources in the DataFrame
        vehicle_data.loc[index, 'resources'] = resources

    return vehicle_data




# Function to select the group leader
def select_group_leader(vehicle_data, random_cell_id):
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






vehicle_data = calculate_direct_trust(vehicle_data, random_cell_id)
vehicle_data = calculate_indirect_trust(vehicle_data, random_cell_id)
vehicle_data = calculate_total_trust(vehicle_data, random_cell_id)
vehicle_data = calculate_distance(vehicle_data, random_cell_id, cell_size=500)
vehicle_data = evaluate_resources(vehicle_data, random_cell_id)
vehicle_data = select_group_leader(vehicle_data, random_cell_id)


# Save the DataFrame back to the CSV file after all functions have been called
vehicle_data.to_csv('vehicle_data.csv', index=False)





