from enum import Enum


class RoadType(Enum):
    Straight = 1
    CurveRight = 2
    Crest = 3
    CurveLeft = 4
    Sag = 5
    All = 6

    # name should return the name of the road type
    def name(self):
        if self == 1:
            return "Straight"
        elif self == 2:
            return "Curve Right"
        elif self == 3:
            return "Crest"
        elif self == 4:
            return "Curve Left"
        elif self == 5:
            return "Sag"
        elif self == 6:
            return "All"
        else:
            return "Unknown"


class KPI(Enum):
    LightIntensity = "lightIntensity"
    RainIntensity = "rainIntensity"
    FogDensity = "fogDensity"
    TestNumber = "testNumber"
    VehicleSpeed = "vehicleSpeed"

    # name should return the name of the road type
    def name(self):
        if self == KPI.LightIntensity:
            return "Light Intensity"
        elif self == KPI.RainIntensity:
            return "Rain Intensity"
        elif self == KPI.FogDensity:
            return "Fog Density"
        elif self == KPI.TestNumber:
            return "Test Number"
        elif self == KPI.VehicleSpeed:
            return "Vehicle Speed"
        else:
            return "Unknown"


class CheckType(Enum):
    Under110 = "under110"
    FirstFullBrake = "firstFullBrake"
    FullBrakePlusReactionTime = "fullBrakePlusReactionTime"
    ReleaseOfAccelerator = "releaseOfAccelerator"
    ReactionAccelToBrake = "reactionAccelToBrake"


    # define a getter for each check type to get its x axis label
    def xAxis(self):
        if self == CheckType.Under110:
            return "Distance to Obstacle at time of reaction (m)"
        elif self == CheckType.FirstFullBrake:
            return "Distance to Obstacle at time of reaction (m)"
        elif self == CheckType.ReleaseOfAccelerator:
            return "Distance to Obstacle at time of reaction (m)"
        elif self == CheckType.FullBrakePlusReactionTime:
            return "Distance to Obstacle at time of reaction (m)"
        elif self == CheckType.ReactionAccelToBrake:
            return "Reaction Time (s)"
        else:
            return "Unknown"

    def title(self):
        if self == CheckType.Under110:
            return "Stop Distance"
        elif self == CheckType.FirstFullBrake:
            return "Stop Distance"
        elif self == CheckType.FullBrakePlusReactionTime:
            return "Stop Distance"
        elif self == CheckType.ReleaseOfAccelerator:
            return "Stop Distance"
        elif self == CheckType.ReactionAccelToBrake:
            return "Reaction Time"

