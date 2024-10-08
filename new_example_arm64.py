from arm64.hallway_simulator_module.HallwaySimulator import HallwaySimulator, BulkHallwaySimulator
import os
import json

os.system("pwd")
"""
hallways_list: list of json object:
            [
                {
                    "hallway_id": "hallway_id",
                    "length": 0,
                    "width": 0,
                    "agents_distribution": X% # percentage of people in this hallway compared to the entire map
                },
                ...
            ]
"""
hallways_list = [
    {
        "hallway_id": "hallway_1",
        "length": 66,
        "width": 4,
        "agents_distribution": 15
    },
    {
        "hallway_id": "hallway_2",
        "length": 66,
        "width": 4,
        "agents_distribution": 12
    }
]

functions_list = [
    "y = 34 * x + 32 (0,50)",
    "y = 3 * x + -100 (60,500)"
]

"""
events_list: list of json object:
            [
                {
                    "AgvIDs": [],
                    "AgvDirections": [],
                    "time_stamp": 0,
                    "hallway_id": "hallway_id"
                }
            ]
"""
events_list = [
    {
        "AgvIDs": [0, 1],
        "AgvDirections": [0, 1],
        "time_stamp": 0,
        "hallway_id": "hallway_1"
    }
]
HallwaySimulator().full_clean()
bulk = BulkHallwaySimulator("test", 800, hallways_list, functions_list, events_list)
output = bulk.run_simulation()
pretty_output = json.dumps(output, indent=4)
print(pretty_output) # [(AGV ID, Time),...]