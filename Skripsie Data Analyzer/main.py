import json
import math
import os
import sys

from IndividualData import *
from calculators import *
from enums import *
from mapData import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def GetListOfDirs():
    # return a list of all folders in the "Saves" directory
    return os.listdir("Saves")


def GetListOfFiles():
    dirs = GetListOfDirs()
    files = []
    print(dirs)
    for dir in dirs:
        # return a list of all files in each folder
        for subdir in os.listdir("Saves/" + dir):
            files.append("Saves/" + dir + "/" + subdir)
    return files


def GetStopDistances(roadType=RoadType.Straight, kpi=KPI.LightIntensity, method=CheckType.Under110):
    # return a list of all stop distances for the given road type
    roadType = roadType.value
    files = GetListOfFiles()
    # print(files)

    plt.figure(figsize=(7, 5))

    stopDistances = []
    for file in files:
        # open the file and read its JSON data
        with open(file, "r") as f:
            data = json.load(f)
            if len(data["mapName"].split(" - ")) <= 1:
                continue
            mapVal = int(data["mapName"].split(" - ")[1].replace("[", "").replace("]", "")) % 5

            if mapVal == 0:
                mapVal = 5
            # print(str(mapVal) + "for " + data["mapName"])

            if mapVal == roadType or roadType == RoadType.All.value:
                # print("Checking " + data["mapName"] + "...")
                PlotPoint(data, kpi, method=method)
                # print(file)

    # set the plot min x to 0
    # plt.xlim(0)
    # set the plot min y to 0
    plt.ylim(0)

    # set the plot title
    plt.title(f"{CheckType.title(method)} vs {KPI.name(kpi)} on {RoadType.name(roadType)} Roads")
    # set the x axis label
    plt.xlabel(CheckType.xAxis(method))
    # set the y axis label
    plt.ylabel(KPI.name(kpi))

    # show the plot
    plt.legend()
    # set the legend position
    plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))

    # set the left border size to 1
    plt.subplots_adjust(right=0.8)

    plt.show()


dataLevels = {}

usedLabelList = []
def PlotPoint(data, kpi=KPI.LightIntensity, method=CheckType.Under110):
    if method == CheckType.Under110:
        distance, speed = CalculateStopDistanceWithLessThan110(data)
    elif method == CheckType.FirstFullBrake:
        distance, speed = CalculateStopDistanceWithFirstFullBrake(data)
    elif method == CheckType.FullBrakePlusReactionTime:
        distance, speed = CalculateStopDistanceWithFullBrakePlusReactionTime(data)
    elif method == CheckType.ReleaseOfAccelerator:
        distance, speed = CalculateStopDistanceWithReleaseOfAccelerator(data)
    elif method == CheckType.ReactionAccelToBrake:
        distance, speed = CalculateReactionTimeWithReactionAccelToBrake(data)
    else:
        distance = None
        speed = None

    if distance is None or distance < 0 or speed is None or speed < 0 or 0.713 < distance < 0.715:
        return
    if speed > 130 or speed < 110:
        return
    if "Curved 2" in data["mapName"]:
        val = - distance
    else:
        val = distance

    stdValues = {
        "lightIntensity": 8.0,
        "rainIntensity": 1.0,
        "fogDensity": 1000.0
    }

    mapVal = int(data["mapName"].split(" - ")[1].replace("[", "").replace("]", ""))

    # if part of control (val < 6), color green with legend "control"
    # if part of test (val < 11), color red with legend "light"
    # if part of test (val < 16), color blue with legend "rain"
    # if part of test (val < 21), color purple with legend "fog"
    # if part of test (val < 26), color yellow with legend "all"
    label = ""
    if mapVal < 6:
        color = "palegreen"
        label = "Control"
    elif mapVal < 11:
        color = "cornflowerblue"
        label = "Night/Dusk"
    elif mapVal < 16:
        color = "powderblue"
        label = "Rain"
    elif mapVal < 21:
        color = "gainsboro"
        label = "Fog"
    else:
        color = "orchid"
        label = "Mixed"



    # plot the point
    # assign the point to the appropriate group
    if kpi != KPI.TestNumber and kpi != KPI.VehicleSpeed:
        plt.scatter(val, mapDetails[data["mapName"]][kpi.value], color=color, label=label)
    elif kpi == KPI.TestNumber:
        if label not in usedLabelList:
            plt.scatter(val, mapVal, color=color, label=label)
            usedLabelList.append(label)
        else:
            plt.scatter(val, mapVal, color=color)
    elif kpi == KPI.VehicleSpeed:
        plt.scatter(val, speed, color=color, label=label)
    # label the point

    # print the stop time, the map name and the participant number
    print(f"Stop time: {distance} seconds on {data['mapName']} with speed {speed} km/h")


# check out vppp sports vs driving assist modes

def PlotSpeedAtDistance(roadType=RoadType.Straight, method=CheckType.Under110):
    # return a list of all stop distances for the given road type
    roadType = roadType.value
    files = GetListOfFiles()
    # print(files)



    values = [{} for _ in range(5)]
    for file in files:
        # open the file and read its JSON data
        with open(file, "r") as f:
            data = json.load(f)
            if len(data["mapName"].split(" - ")) <= 1:
                continue

            if IdentifyOutliers(data):
                #ShowPath(file)
                print("Outlier found in " + file)
                continue

            mapVal = int(data["mapName"].split(" - ")[1].replace("[", "").replace("]", ""))
            index = (mapVal - 1) / 5
            index = int(index)
            mapVal = mapVal % 5

            if mapVal == 0:
                mapVal = 5
            # print(str(mapVal) + "for " + data["mapName"])

            if mapVal == roadType or roadType == RoadType.All.value:
                #print("Checking " + data["mapName"] + " and has index of " + str(index) + "...")

                values[index] = AddSpeedPerDistance(values[index], data)
                # print(file)

    # set the plot min x to 0
    # plt.xlim(0)
    # set the plot min y to 0
    # plt.ylim(0)

    # set the plot title
    plt.title(f"{CheckType.title(method)} on {RoadType.name(roadType)} Roads")
    # set the x axis label
    plt.xlabel(CheckType.xAxis(method))
    # set the y axis label
    plt.ylabel("Speed")

    # sort each dict in values by key
    for i in range(0, len(values)):
        values[i] = dict(sorted(values[i].items()))



    # set the plot to have two subplots, one next to the other.
    # the first subplot needs to have a width of 10, and the second needs to have a width of 3
    figs, axs = plt.subplots(1, 2, figsize=(13, 3), gridspec_kw={'width_ratios': [6, 4]})

    plt.subplots_adjust(bottom=0.2, right= 0.875)

    crossPoints = []

    for myDict in values:
        upStdSpeedList = []
        speedList = []
        downStdSpeedList = []
        distanceList = []
        for key in myDict:
            upStdSpeedList.append(np.mean(myDict[key]) + np.std(myDict[key]))
            speedList.append(np.mean(myDict[key]))
            downStdSpeedList.append(np.mean(myDict[key]) - np.std(myDict[key]))
            distanceList.append(key)

        convolveSize = 30
        if len(speedList) > 0 and len(upStdSpeedList) > 0 and len(downStdSpeedList) > 0:
            # smooth the data with a cast of 5
            speedList = np.convolve(speedList, np.ones(convolveSize), 'same') / convolveSize
            upStdSpeedList = np.convolve(upStdSpeedList, np.ones(convolveSize), 'same') / convolveSize
            downStdSpeedList = np.convolve(downStdSpeedList, np.ones(convolveSize), 'same') / convolveSize

            color = None
            label = None
            if values.index(myDict) == 0:
                label = "Control"
                color = "palegreen"
            elif values.index(myDict) == 1:
                label = "Night"
                color = "cornflowerblue"
            elif values.index(myDict) == 2:
                label = "Fog"
                color = "powderblue"
            elif values.index(myDict) == 3:
                label = "Rain"
                color = "gainsboro"
            elif values.index(myDict) == 4:
                label = "Mixed"
                color = "orchid"



            axs[0].plot(distanceList, speedList, color=color, label=label)
            axs[1].plot(distanceList, speedList, color=color, label=label)
            axs[0].fill_between(distanceList, upStdSpeedList, downStdSpeedList, color=color, alpha=0.2)
            axs[1].fill_between(distanceList, upStdSpeedList, downStdSpeedList, color=color, alpha=0.2)

            targetAngle = [10, 10, 20, 10, 20][roadType - 1]
            targetDistance = [400, 210, 140, 210, 210][roadType - 1]

            #print("Len of speedlist is " + str(len(speedList)) + " and len of distancelist is " + str(len(distanceList)) + " and len of upstdspeedlist is " + str(len(upStdSpeedList)) + " and len of downstdspeedlist is " + str(len(downStdSpeedList)))
            for i in range(len(speedList) - 1, 1, -1):
                angle = (speedList[i] - speedList[i - 1]) / (distanceList[i] - distanceList[i - 1])
                angle = math.degrees(math.atan(angle))

                if angle >= targetAngle and distanceList[i] < targetDistance:
                    print(f"Angle of {angle} at {distanceList[i]} meters, speed {speedList[i]}, with a deviation of {speedList[i] - upStdSpeedList[i]} on {label} road")
                    crossPoints.append((distanceList[i], speedList[i], color))
                    break

    colors = ["darkgreen", "darkblue", "darkcyan", "darkgrey", "darkmagenta"]

    for point in crossPoints:
        axs[0].scatter(point[0], point[1], color=colors[crossPoints.index(point)], marker="x", s=50)
        axs[1].scatter(point[0], point[1], color=colors[crossPoints.index(point)], marker="x", s=50)

    # add axis labels
    axs[0].set_xlabel("Distance (m) to Obstacle")
    axs[1].set_xlabel("Distance (m) to Obstacle")
    axs[0].set_ylabel("Speed (km/h)")
    axs[1].set_ylabel("Speed (km/h)")

    axs[0].set_title(f"Mean Speed and Reaction Distance on {RoadType.name(roadType)} Roads")
    axs[1].set_title(f"Mean Speed and Reaction Distance on {RoadType.name(roadType)} Roads (Zoomed)")

    # plot a red dotted line at x = 0
    axs[0].axvline(x=0, color="crimson", linestyle=":", label="Obstacle")
    # draw a rectangle from (-50, 0) to (250, 150)
    axs[0].add_patch(Rectangle((-50, 0), 300, 140, color="crimson", alpha=0.1, fill=False))

    axs[1].axvline(x=0, color="crimson", linestyle=":", label="Obstacle")

    # add a legend
    #axs[0].legend(loc="upper right", bbox_to_anchor=(1.15, 1.0))
    axs[0].legend()
    # invert x axis
    axs[0].invert_xaxis()
    # set the x lim to 250
    axs[1].set_xlim(-50, 250)
    axs[1].invert_xaxis()

    plt.show()


if __name__ == "__main__":
    GetStopDistances(roadType=RoadType.All, kpi=KPI.TestNumber, method=CheckType.ReactionAccelToBrake)

    #for roadType in RoadType:
    #    PlotSpeedAtDistance(roadType=roadType)
    #PlotSpeedAtDistance(roadType=RoadType.Straight)

    # PlotMeansAndStds(roadType=RoadType.All, kpi=KPI.LightIntensity, method=CheckType.ReactionAccelToBrake, normalized=False)
    # get a single person's tests and compare to themself (avg. and std. var.)
    # compare mean stop distance vs theory

    # Samantha Stuurman
    # sbstuurman@sun.ac.za
    # K1859

    # receipt, bank-state, proof of email
