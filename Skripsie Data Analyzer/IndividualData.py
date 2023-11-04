import numpy as np

from calculators import *
from enums import *
from mapData import *

import matplotlib.pyplot as plt

def getFolders(root):
    # return a list of all the folders in the root folder
    import os
    return [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]

def determineDistancesForConditions(folder, roadType, kpi, method, normalized=False):
    # for each file in the folder, determine the stop distance for the given conditions
    import json
    import os
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    distances = {}
    for file in files:
        with open(folder + "/" + file, "r") as f:
            data = json.load(f)
            if len(data["mapName"].split(" - ")) <= 1:
                continue
            mapVal = int(data["mapName"].split(" - ")[1].replace("[", "").replace("]", ""))
            mapValMod = mapVal % 5
            if mapValMod == 0:
                mapValMod = 5

            if roadType.value == mapValMod or roadType == RoadType.All:
                if method == CheckType.Under110:
                    distance = CalculateStopDistanceWithLessThan110(data)
                elif method == CheckType.FirstFullBrake:
                    distance = CalculateStopDistanceWithFirstFullBrake(data)
                elif method == CheckType.ReactionAccelToBrake:
                    distance = CalculateStopDistanceWithReleaseOfAccelerator(data)
                elif method == CheckType.ReleaseOfAccelerator:
                    distance = CalculateStopDistanceWithReleaseOfAccelerator(data)


                if distance is not None:
                    if mapValMod == 4:
                        distance *= -1

                distances[mapVal] = distance

    if normalized:
        if 1 not in distances.keys():
            return None
        if distances[1] == 0 or distances[1] is None:
            return None
        originalVal = distances[1]
        for key in distances.keys():

            if distances[key] is not None:
                distances[key] = distances[key] / originalVal
    return distances

def calculateAvgAndStdForRoadType(roadType, kpi, method, normalized=False):
    # for each folder in the Saves directory, determine the stop distance for the given conditions
    folders = getFolders("Saves")
    distances = {}
    for folder in folders:
        result = determineDistancesForConditions("Saves/" + folder, roadType, kpi, method, normalized=normalized)
        if result is not None:
            for key in result.keys():
                if key not in distances.keys():
                    distances[key] = []
                if result[key] is not None:
                    distances[key].append(result[key])

    print(distances)

    Means = {}
    Stds = {}

    for key in distances.keys():
        Means[key] = np.mean(distances[key])
        Stds[key] = np.std(distances[key])

    return Means, Stds

def PlotMeansAndStds(roadType, kpi, method, normalized = False):
    mean, std = calculateAvgAndStdForRoadType(roadType, kpi, method, normalized=normalized)

    # draw points with the mean as x value, and y value as the key
    # draw a line from the mean - std to the mean + std as the error bar

    x = []
    y = []
    yerr = []
    for key in mean.keys():
        x.append(mean[key])
        y.append(key)
        yerr.append(std[key])

    plt.errorbar(x, y, xerr=yerr, fmt='o')
    plt.show()