import json
import matplotlib.pyplot as plt
import calculations
# Step 1: Load the JSON file
file_paths = \
    [
        r'C:\Users\chris\OneDrive\Desktop\Programming\Python Projects\Skripsie Data Visualizer\Saves\23\drive_data_22.json',  # Replace with the actual file path
        r'C:\Users\chris\OneDrive\Desktop\Programming\Python Projects\Skripsie Data Visualizer\Saves\7\drive_data_1.json',  # Replace with the actual file path
        r'C:\Users\chris\OneDrive\Desktop\Programming\Python Projects\Skripsie Data Visualizer\Saves\10\drive_data_37.json',  # Replace with the actual file path

    ]
def ShowPath(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

    # Step 2: Extract relevant data
    map_name = data.get("mapName", "Unknown Map")
    light_intensity = data.get("lightIntensity", 0.0)
    fog_density = data.get("fogDensity", 0.0)
    rain_intensity = data.get("rainIntensity", 0.0)
    samples = data.get("data", [])

    # Extract individual data points

    start_time = samples[0]["time"]

    times = [sample["time"] - start_time for sample in samples]
    speeds = [sample["speed"] for sample in samples]
    distances_to_obstacle = [sample["distanceToObstacle"] for sample in samples]
    distances_to_vehicle = [sample["distanceToVehicle"] for sample in samples]
    acceleration_pedal_input = [sample["accelerationPedalInput"] for sample in samples]
    brake_pedal_input = [sample["brakePedalInput"] for sample in samples]
    steering_input = [sample["steeringInput"] for sample in samples]

    plt.figure(figsize=(10,3))
    # set the figure bottom to 0.1 instead of 0.0
    plt.subplots_adjust(bottom=0.2)
    plt.plot(times, acceleration_pedal_input, color = 'lightseagreen', label = 'Acceleration Pedal Input')
    plt.xlabel('Time')
    plt.ylabel('Pedal Input')
    plt.title('Pedal Input vs. Time')

    plt.plot(times, brake_pedal_input, color = 'orchid', label = 'Brake Pedal Input')
    plt.xlabel('Time')
    plt.ylabel('Pedal Input')
    plt.title('Pedal Input vs. Time')

    # draw a y line at CalculateStopDistanceWithFullBrakePlusReactionTime
    # draw a y line at CalculateStopDistanceWithReleaseOfAccelerator
    # draw a y line at CalculateStopDistanceWithFirstFullBrake

    full_brake_plus_reaction_time = calculations.CalculateStopDistanceWithFullBrakePlusReactionTime(data) - start_time
    release_of_accelerator = calculations.CalculateStopDistanceWithReleaseOfAccelerator(data) - start_time
    first_full_brake = calculations.CalculateStopDistanceWithFirstFullBrake(data) - start_time

    # label the lines

    plt.axvline(x=full_brake_plus_reaction_time, color='r', linestyle='dashdot', label='Full Brake + Reaction Time')
    plt.axvline(x=release_of_accelerator, color='g', linestyle=':', label='Release of Accelerator')
    plt.axvline(x=first_full_brake, color='b', linestyle='--', label='First Brake to Stop')

    print(full_brake_plus_reaction_time)
    print(release_of_accelerator)
    print(first_full_brake)

    plt.legend()

    # set the size of the plot window


    plt.show()

if __name__ == "__main__":
    for file_path in file_paths:
        ShowPath(file_path)