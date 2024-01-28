import random
import pandas as pd
import math
import time

# Read the CSV file
vehicle_data = pd.read_csv('vehicle_data.csv')




def get_surrounding_vehicles(vehicle_id):
    # Get the cell ID for the vehicle
    cell_id = vehicle_data[vehicle_data['vehicle_id'] == vehicle_id]['cell_id'].values[0]

    # Get the list of vehicles in the same cell
    cell_vehicles = vehicle_data[vehicle_data['cell_id'] == cell_id]['vehicle_id'].values

    # Remove the current vehicle from the list
    cell_vehicles = cell_vehicles[cell_vehicles != vehicle_id]

    return cell_vehicles




def get_position(vehicle_id):
    # This function returns the position (longitude, latitude) of the vehicle
    vehicle = vehicle_data[vehicle_data['vehicle_id'] == vehicle_id]
    return vehicle['longitude'].values[0], vehicle['latitude'].values[0]

def calculate_deviations(vehicle_id, surrounding_vehicles):
    vehicle_position = get_position(vehicle_id)
    deviations = []

    for surrounding_vehicle in surrounding_vehicles:
        surrounding_vehicle_position = get_position(surrounding_vehicle)
        deviation = math.sqrt((vehicle_position[0] - surrounding_vehicle_position[0])**2 + 
                              (vehicle_position[1] - surrounding_vehicle_position[1])**2)
        deviations.append((surrounding_vehicle, deviation))

    return deviations

def select_vehicle_with_min_deviation(deviations):
    # Select the vehicle with the minimum deviation
    min_deviation_vehicle, min_deviation = min(deviations, key=lambda x: x[1])
    return min_deviation_vehicle




def send_lbs_request(vehicle_id, message, timestamp, server_info):
    # Simulate sending a LBS request
    request = {
        'vehicle_id': random.randint(1000, 9999),  # Assign a random ID
        'message': message,
        'timestamp': timestamp,
        'server_info': server_info
    }
    print(f"Sending request from vehicle {request['vehicle_id']} to server...")
    return request

def receive_lbs_response(request):
    # Simulate receiving a LBS response
    time.sleep(random.randint(1, 3))  # Simulate network delay
    response = {
        'vehicle_id': request['vehicle_id'],
        'message': 'Response to your request',
        'timestamp': time.time(),
        'server_info': request['server_info']
    }
    print(f"Received response from server to vehicle {request['vehicle_id']}")
    return response




def filter_messages_based_on_location(vehicle_id, messages):
    # Get the vehicle's location
    vehicle_location = get_position(vehicle_id)

    # Filter the messages based on the vehicle's location
    filtered_messages = [message for message in messages if is_relevant(message, vehicle_location)]

    return filtered_messages

def is_relevant(message, location):
    # Check if the message's location is the same as the given location
    return message['location'] == location





def main():
    # Choose a vehicle to test the functions
    test_vehicle_id = vehicle_data['vehicle_id'].values[0]

    # Test get_surrounding_vehicles
    surrounding_vehicles = get_surrounding_vehicles(test_vehicle_id)
    print(f"Surrounding vehicles of {test_vehicle_id}: {surrounding_vehicles}")

    # Test get_position
    position = get_position(test_vehicle_id)
    print(f"Position of {test_vehicle_id}: {position}")

    # Test calculate_deviations
    deviations = calculate_deviations(test_vehicle_id, surrounding_vehicles)
    print(f"Deviations of surrounding vehicles from {test_vehicle_id}: {deviations}")

    # Test select_vehicle_with_min_deviation
    min_deviation_vehicle = select_vehicle_with_min_deviation(deviations)
    print(f"Vehicle with minimum deviation from {test_vehicle_id}: {min_deviation_vehicle}")

    # Test send_lbs_request and receive_lbs_response
    request = send_lbs_request(test_vehicle_id, 'Test message', time.time(), 'Test server info')
    response = receive_lbs_response(request)
    print(f"Response to request from {test_vehicle_id}: {response}")

    # Test filter_messages_based_on_location and is_relevant
    # For this test, we'll use some dummy messages
    messages = [{'vehicle_id': v, 'location': get_position(v), 'content': 'Test message'} for v in surrounding_vehicles]
    filtered_messages = filter_messages_based_on_location(test_vehicle_id, messages)
    print(f"Messages relevant to {test_vehicle_id}: {filtered_messages}")

if __name__ == "__main__":
    main()









    