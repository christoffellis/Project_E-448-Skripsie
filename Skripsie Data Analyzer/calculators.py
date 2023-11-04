import copy
import json
import matplotlib.pyplot as plt


def CalculateStopDistanceWithLessThan110(testData):
    data = testData["data"]
    last_speed_above_110 = None

    for item in data:
        speed = item["speed"]
        if speed > 110:
            last_speed_above_110 = item

    if last_speed_above_110 is not None:
        distance_diff = last_speed_above_110["distanceToObstacle"] - last_speed_above_110["distanceToVehicle"]
        # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
        return distance_diff, last_speed_above_110["speed"]
    else:
        # print("No data point with speed above 110 found.")
        pass


def CalculateStopDistanceWithFirstFullBrake(testData, asTimeStamp=False):
    # split the data is half, and check the last section of the data.
    # from the back, check to see the if the break is moved from 0 to 1, over a span of 25 data points or less
    # if so, return the distance to the obstacle at that point, at the start of the brake increase
    # if not, check for the next time the break is moved from 0 to 1
    # if no such point is found, return None
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    lastBrakeIncrease = None
    for i in range(dataLength - 1, halfDataLength, -1):
        if data[i]["brakePedalInput"] > 0 and data[i - 1]["brakePedalInput"] == 0 and data[i]["speed"] > 20 and data[i + 50]["brakePedalInput"] != 0:
            lastBrakeIncrease = i
            break

    if lastBrakeIncrease is not None:
        distance_diff = data[lastBrakeIncrease]["distanceToObstacle"] - data[lastBrakeIncrease]["distanceToVehicle"]
        # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
        if asTimeStamp:
            return data[lastBrakeIncrease]["time"], data[lastBrakeIncrease]["speed"]
        else:
            return distance_diff, data[lastBrakeIncrease]["speed"]
    else:
        # print("No data point with speed above 110 found.")
        pass


def CalculateStopDistanceWithFullBrakePlusReactionTime(testData, asTimeStamp=False):
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    lastBrakeIncrease = None
    for i in range(dataLength - 1, halfDataLength, -1):
        if data[i]["brakePedalInput"] > 0 and data[i - 1]["brakePedalInput"] == 0 and data[i]["speed"] > 20:
            lastBrakeIncrease = i
            break

    if lastBrakeIncrease is not None:
        reactionTime, _ = CalculateReactionTimeWithReactionAccelToBrake(testData)
        for i in range(lastBrakeIncrease, 0, -1):
            if data[lastBrakeIncrease]["time"] - data[i - 1]["time"] > reactionTime:
                distance_diff = data[i]["distanceToObstacle"] - data[i]["distanceToVehicle"]
                # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
                if asTimeStamp:
                    return data[i]["time"], data[i]["speed"]
                else:
                    return distance_diff, data[i]["speed"]

    return None, None


def CalculateStopDistanceWithReleaseOfAccelerator(testData, asTimeStamp=False):
    # get the distance between the car and the obstacle at the point where the accelerator is released
    # check for the first point where the accelerator is released before the car goes below 60
    # if no such point is found, return None
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    lastAcceleratorRelease = None
    for i in range(halfDataLength, dataLength - 1, 1):
        if data[i]["accelerationPedalInput"] == 0 and data[i]["speed"] >= 50:
            lastAcceleratorRelease = i

            for j in range(i, dataLength):
                if data[j]["accelerationPedalInput"] > 0 and data[j]["speed"] >= 50:
                    lastAcceleratorRelease = None
                    break

            if lastAcceleratorRelease is not None:
                break

    if lastAcceleratorRelease is not None:
        distance_diff = data[lastAcceleratorRelease]["distanceToObstacle"] - data[lastAcceleratorRelease][
            "distanceToVehicle"]
        # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
        if asTimeStamp:
            return data[lastAcceleratorRelease]["time"], data[lastAcceleratorRelease]["speed"]
        else:
            return distance_diff, data[lastAcceleratorRelease]["speed"]


def CalculateReactionTimeWithReactionAccelToBrake(testData):
    # get the distance between the car and the obstacle at the point where the accelerator is released
    # check for the first point where the accelerator is released before the car goes below 60
    # if no such point is found, return None
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    stopTime = None
    speed = None
    timeFirstAccelRelease = None
    timeFirstBrakeIncrease = None
    speed1 = None
    speed2 = None

    val = CalculateStopDistanceWithReleaseOfAccelerator(testData, asTimeStamp=True)
    if val is not None:
        timeFirstAccelRelease, speed1 = val
    val = CalculateStopDistanceWithFirstFullBrake(testData, asTimeStamp=True)
    if val is not None:
        timeFirstBrakeIncrease, speed2 = val

    if timeFirstAccelRelease is not None and timeFirstBrakeIncrease is not None:
        stopTime = timeFirstBrakeIncrease - timeFirstAccelRelease
    else:
        stopTime = 0.714

    speed = speed1 if speed1 is not None else speed2

    if stopTime is not None:
        if stopTime < 0:
            stopTime = 0.714
        if stopTime > 1.197:
            stopTime = 0.714
        mapVal = int(testData["mapName"].split(" - ")[1].replace("[", "").replace("]", ""))
        if mapVal % 5 == 4:
            stopTime *= -1

        return stopTime, speed
    else:
        return 0.714, speed


def AddSpeedPerDistance(dict, testData):
    originalDict = copy.deepcopy(dict)
    data = testData["data"]

    mapVal = int(testData["mapName"].split(" - ")[1].replace("[", "").replace("]", "")) % 5
    print(mapVal)

    distanceToObstacle = data[-10]["distanceToObstacle"]
    hasDrivenFarOver = False
    hasAddedAtDistance = None
    for i in range(0, len(data)):
        distance = round(data[i]["distanceToVehicle"], 0)
        speed = round(data[i]["speed"], 0)

        if mapVal != 4:
            if distanceToObstacle - distance not in dict:
                dict[distanceToObstacle - distance] = [speed]
            elif hasAddedAtDistance != distance:
                dict[distanceToObstacle - distance].append(speed)
                hasAddedAtDistance = distance
        else:
            if distance - distanceToObstacle not in dict:
                dict[distance - distanceToObstacle] = [speed]
            elif hasAddedAtDistance != distance:
                dict[distance - distanceToObstacle].append(speed)
                hasAddedAtDistance = distance

        if mapVal == 1:  # straight
            if distanceToObstacle - distance < -200 or distanceToObstacle - distance > 1250:
                hasDrivenFarOver = True
        elif mapVal == 3:
            if distanceToObstacle - distance < -200:
                hasDrivenFarOver = True

    minDistance = min(dict.keys())
    for i in range(int(minDistance * 10), -1000, -1):
        dist = i / 10
        if dist not in dict:
            dict[dist] = [0]

    if not hasDrivenFarOver:
        return dict
    else:
        return originalDict


def IdentifyOutliers(testData):
    data = testData["data"]

    if int(testData["mapName"].split(" - ")[1].replace("[", "").replace("]", "")) % 5 == 4:
        return False

    for dataPoint in data:
        if dataPoint["distanceToObstacle"] - dataPoint["distanceToVehicle"] > 200:
            # print(dataPoint["distanceToObstacle"] - dataPoint["distanceToVehicle"])
            return False


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

    plt.figure(figsize=(10, 3))
    # set the figure bottom to 0.1 instead of 0.0
    plt.subplots_adjust(bottom=0.2)

    # turn the plot to 2 subplots and plot the following on the first plot
    plt.subplot(2, 1, 1)

    plt.plot(times, acceleration_pedal_input, color='lightseagreen', label='Acceleration Pedal Input')
    plt.xlabel('Time')
    plt.ylabel('Pedal Input')
    plt.title('Pedal Input vs. Time')

    plt.plot(times, brake_pedal_input, color='orchid', label='Brake Pedal Input')
    plt.xlabel('Time')
    plt.ylabel('Pedal Input')
    plt.title('Pedal Input vs. Time')

    plt.subplot(2, 1, 2)
    plt.plot(times, distances_to_vehicle, color='darkorange', label='Speed')
    plt.plot(times, distances_to_obstacle, color='royalblue', label='Speed')

    plt.legend()

    # set the size of the plot window

    plt.show()
