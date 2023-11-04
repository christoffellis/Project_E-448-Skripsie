## Project (E) - 448
As part of my final year submission for my degree in BEng (Electric and Electronic), I had to analyze and visualize data. 

The analyzers used can be found in this repository.

### Using this code to view the data
Due to this data using real participant data, none of that data may be shared, unless it is requested for other research. Thus, the data is excluded from this repository. Should you wish to view your data with this tool, you can add it to each of the folders in the main repository, under a Saves folder, and in sub-folders, such ass "Save 1".
The project hierarchy should look like this:
```
  - Skripsie Data Analyzer
    - Saves
      - 1
        - 1_1.json
        - 1_2.json
        - ...
      - 2
        - 2_1.json
        - 2_2.json
  - Skripsie Data Visualizer
    - Saves
      - 1
        - 1_1.json
        - 1_2.json
        - ...
      - 2
        - 2_1.json
        - 2_2.json
```

With the JSON format as follows:
```
{
    "mapName": string,
    "lightIntensity": float,
    "fogDensity": float,
    "rainIntensity": float,
    "data": [
        {
            "time": float,
            "speed": float,
            "distanceToObstacle": float,
            "distanceToVehicle": float,
            "accelerationPedalInput": float,
            "brakePedalInput": float,
            "steeringInput": float
        },
        {
            ...
        }
    ]
}
```
