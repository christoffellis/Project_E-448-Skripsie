def CalculateStopDistanceWithFirstFullBrake(testData):
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
        if data[i]["brakePedalInput"] > 0 and data[i - 1]["brakePedalInput"] == 0 and data[i]["speed"] > 20:
            lastBrakeIncrease = i
            break

    if lastBrakeIncrease is not None:
        distance_diff = data[lastBrakeIncrease]["distanceToObstacle"] - data[lastBrakeIncrease]["distanceToVehicle"]
        # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
        return data[lastBrakeIncrease]["time"]
    else:
        # print("No data point with speed above 110 found.")
        pass

def CalculateStopDistanceWithFullBrakePlusReactionTime(testData):
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    lastBrakeIncrease = None
    for i in range(dataLength - 1, halfDataLength, -1):
        if data[i]["brakePedalInput"] > 0 and data[i - 1]["brakePedalInput"] == 0 and data[i]["speed"] > 20:
            lastBrakeIncrease = i
            break

    if lastBrakeIncrease is not None:
        reactionTime = CalculateReactionTimeWithReactionAccelToBrake(testData)
        for i in range(lastBrakeIncrease, 0, -1):
            if data[lastBrakeIncrease]["time"] - data[i - 1]["time"] > reactionTime:
                distance_diff = data[i]["distanceToObstacle"] - data[i]["distanceToVehicle"]
                # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
                return data[i]["time"]

def CalculateStopDistanceWithReleaseOfAccelerator(testData):
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
                if data[j]["accelerationPedalInput"] > 0:
                    lastAcceleratorRelease = None
                    break

            if lastAcceleratorRelease is not None:
                break


    if lastAcceleratorRelease is not None:
        distance_diff = data[lastAcceleratorRelease]["distanceToObstacle"] - data[lastAcceleratorRelease][
            "distanceToVehicle"]
        # print(f"Difference between distance to obstacle and distance to vehicle: {distance_diff}")
        return data[lastAcceleratorRelease]["time"]

def CalculateReactionTimeWithReactionAccelToBrake(testData):
    # get the distance between the car and the obstacle at the point where the accelerator is released
    # check for the first point where the accelerator is released before the car goes below 60
    # if no such point is found, return None
    data = testData["data"]
    dataLength = len(data)
    halfDataLength = int(dataLength / 2)
    stopTime = None

    timeFirstAccelRelease = CalculateStopDistanceWithReleaseOfAccelerator(testData)
    timeFirstBrakeIncrease = CalculateStopDistanceWithFirstFullBrake(testData)
    if timeFirstAccelRelease is not None and timeFirstBrakeIncrease is not None:
        stopTime = timeFirstBrakeIncrease - timeFirstAccelRelease
    else:
        return 0.714

    print(f"First accel release: {timeFirstAccelRelease}")
    print(f"First brake increase: {timeFirstBrakeIncrease}")
    print(f"Stop time: {stopTime}")


    if stopTime is not None:
        if stopTime > 1.197:
            return 0.714
        mapVal = int(testData["mapName"].split(" - ")[1].replace("[", "").replace("]", ""))
        if mapVal % 5 == 4:
            stopTime *= -1

        return stopTime
    else:
        return 0.714
