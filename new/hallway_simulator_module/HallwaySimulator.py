# This module is used as interface to call and get the simulation results from the hallway simulator
# input: hallway ID, list of AGV IDs, list of AGV directions, number of people in the hallway, human type distribution(lst), time stamp(seconds), event type(0: new_event, 1: update_event(reuse the previous event with new AGV))
# output: Run time of all AGVs (get from json file)

import json
import os
import time
import sys

class HallwaySimulator:
    def __init__(self):
        self.hallway_id = 0 # string
        self.hallway_length = 0 # int
        self.hallway_width = 0 # int
        self.agv_ids = [] # list of int
        self.agv_directions = [] # list of int
        self.num_people = 0 # int
        self.human_type_distribution = [] # list of int
        self.time_stamp = 0 # int
        self.event_type = 0 # int
        self.run_time = [] # list of tuple (AGV ID, run time)

    def set_params(self,
                   hallway_id,
                   hallway_length,
                   hallway_width,
                   agv_ids,
                   agv_directions,
                   num_people,
                   human_type_distribution,
                   time_stamp,
                   event_type):
        self.hallway_id = hallway_id
        self.hallway_length = hallway_length
        self.hallway_width = hallway_width
        self.agv_ids = agv_ids
        self.agv_directions = agv_directions
        self.num_people = num_people
        self.human_type_distribution = human_type_distribution
        self.time_stamp = time_stamp
        self.event_type = event_type

    def json2params(self, json_data):
        self.set_params(
            json_data["hallway_id"],
            json_data["hallway_length"],
            json_data["hallway_width"],
            json_data["agv_ids"],
            json_data["agv_directions"],
            json_data["num_people"],
            json_data["human_type_distribution"],
            json_data["time_stamp"],
            json_data["event_type"]
        )

    def create_json(self):
        """
        json filename: <hallway_id>_<time_stamp>.json
        {
          "numOfAgents": {
            "description": "Number of agents",
            "value": 50
          },
          "TDDegree": {
            "description": "T-Distribution' degree of freedom",
            "value": 15
          },
          "totalCrowdLength": {
            "description": "Crowd total length",
            "value": 50
          },
          "headCrowdLength": {
            "description": "Crowd head/tail length",
            "value": 10
          },
          "crowdWidth": {
            "description": "Crowd width",
            "value": 2
          },
          "acceleration": {
            "description": "Acceleration of AGV",
            "value": 0
          },
          "agvDesiredSpeed": {
            "description": "Desired speed of AGV (m/s)",
            "value": 0.6
          },
          "thresDistance": {
            "description": "Threshold distance for agv to stop when colliding with a person",
            "value": 0.3
          },
          "stopAtHallway": {
            "description": "Percentage of people stopping at the hallway",
            "value": 2
          },
          "p1": {
            "description": "Percentage of agents (No disability, without overtaking behavior)",
            "value": 22
          },
          "p2": {
            "description": "Percentage of agents (No disability, with overtaking behavior)",
            "value": 5
          },
          "p3": {
            "description": "Percentage of agents (Walking with crutches)",
            "value": 17
          },
          "p4": {
            "description": "Percentage of agents (Walking with sticks)",
            "value": 22
          },
          "p5": {
            "description": "Percentage of agents (Wheelchairs)",
            "value": 17
          },
          "p6": {
            "description": "Percentage of agents (The blind)",
            "value": 17
          },
          "hallwayLength": {
            "description": "Hallway length",
            "value": 60
          },
          "hallwayWidth": {
            "description": "Hallway width",
            "value": 6
          },
          "agvDirections": {
            "description": "Run direction of the AGV: left to right (0), right to left (1)",
            "value": [1]
          },
          "agvIDs": {
            "description": "AGV ID",
            "value": [2]
          },
          "timeline_pointer": {
            "description": "Timeline pointer",
            "value": 15
          },
          "hallwayID": {
            "description": "Arc ID",
            "value": "j0"
          },
          "experimentalDeviation": {
            "description": "Experimental deviation (percent)",
            "value": 10
          }
        }
        """
        data = {
            "numOfAgents": {
                "description": "Number of agents",
                "value": self.num_people
            },
            "TDDegree": {
                "description": "T-Distribution' degree of freedom",
                "value": 15
            },
            "totalCrowdLength": {
                "description": "Crowd total length",
                "value": 50
            },
            "headCrowdLength": {
                "description": "Crowd head/tail length",
                "value": 10
            },
            "crowdWidth": {
                "description": "Crowd width",
                "value": 2
            },
            "acceleration": {
                "description": "Acceleration of AGV",
                "value": 0.25
            },
            "agvDesiredSpeed": {
                "description": "Desired speed of AGV (m/s)",
                "value": 0.6
            },
            "thresDistance": {
                "description": "Threshold distance for agv to stop when colliding with a person",
                "value": 0.3
            },
            "stopAtHallway": {
                "description": "Percentage of people stopping at the hallway",
                "value": 2
            },
            "p1": {
                "description": "Percentage of agents (No disability, without overtaking behavior)",
                "value": self.human_type_distribution[0]
            },
            "p2": {
                "description": "Percentage of agents (No disability, with overtaking behavior)",
                "value": self.human_type_distribution[1]
            },
            "p3": {
                "description": "Percentage of agents (Walking with crutches)",
                "value": self.human_type_distribution[2]
            },
            "p4": {
                "description": "Percentage of agents (Walking with sticks)",
                "value": self.human_type_distribution[3]
            },
            "p5": {
                "description": "Percentage of agents (Wheelchairs)",
                "value": self.human_type_distribution[4]
            },
            "p6": {
                "description": "Percentage of agents (The blind)",
                "value": self.human_type_distribution[5]
            },
            "hallwayLength": {
                "description": "Hallway length",
                "value": self.hallway_length
            },
            "hallwayWidth": {
                "description": "Hallway width",
                "value": self.hallway_width
            },
            "agvDirections": {
                "description": "Run direction of the AGV: left to right (0), right to left (1)",
                "value": self.agv_directions
            },
            "agvIDs": {
                "description": "AGV ID",
                "value": self.agv_ids
            },
            "timeline_pointer": {
                "description": "Timeline pointer",
                "value": self.time_stamp
            },
            "hallwayID": {
                "description": "Arc ID",
                "value": f"{self.hallway_id}"
            },
            "experimentalDeviation": {
                "description": "Experimental deviation (percent)",
                "value": 10
            }
        }
        filename = f"data/input/{self.hallway_id}_{self.time_stamp}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        return filename

    def create_map(self):
        """
        map filename: <hallway_id>_<time_stamp>.txt
        1
        6
        J1 2 3 3

        explain:
        <don't care -> keep the same>
        <Hallway width>
        <Hallway ID> <dont_care -> keep the same> <hallway length> <hallway length>
        """
        filename = f"data/input/{self.hallway_id}_{self.time_stamp}.txt"
        with open(filename, "w") as f:
            f.write("1\n")
            f.write(f"{self.hallway_width}\n")
            f.write(f"J{self.hallway_id} 2 {self.hallway_length} {self.hallway_length}")
        return filename

    def run_simulation(self):
        json_file = self.create_json()
        map_file = self.create_map()
        os.system(f"x86_64/hallway_simulator_module/sim/app {json_file} {map_file} {self.event_type}")

        # scan the model/hallway_simulator_module/sim/data/output folder to get the run time of all AGVs (all in json format)
        time.sleep(1)
        files = os.listdir("data/output")
        # result_agv_1.json, result_agv_2.json, ...
        for agv_id in self.agv_ids:
            log_name = f"result_agv_{agv_id}.json"
            for file in files:
                if log_name == file:
                    with open(f"data/output/{file}", "r") as f:
                        data = json.load(f)
                        # "AGVRealTime" is the key to get the run time of the AGV(divided the number to 1000)
                        real_time = int(data["AGVRealTime"]/1000)
                        ID = int(file.split("_")[2].split(".")[0])
                        self.run_time.append((ID, real_time)) # (AGV ID, run time)
        return self.run_time

    def clean(self):
        os.system("rm -rf data/input/*")
        os.system("rm -rf data/output/*")
        # reset all variables
        self.hallway_id = 0
        self.hallway_length = 0
        self.hallway_width = 0
        self.agv_ids = []
        self.agv_directions = []
        self.num_people = 0
        self.human_type_distribution = []
        self.time_stamp = 0
        self.event_type = 0

# new class to perform bulk operations
# input:
"""
{
    "Scenario_ID": "scenario_id",
    "Human_distribution_function": "y=a*x+b (x [from, to])",
    "hallways": [
        "hallway_id_0": {
            height: 0,
            width: 0,
            agv_ids: [],
            agv_directions: [],
            human_type_distribution: [],
            time_stamp: 0
        },
        "hallway_id_1": {
            height: 0,
            width: 0,
            agv_ids: [],
            agv_directions: [],
            human_type_distribution: [],
            time_stamp: 0
        },
        ...
    ]
}
"""
"""
How this works:
generate variables:
json AGV_COMPLETION_LOGS = {
    "AGV_ID": {
        "hallway_id": {
            "time_stamp": time_stamp,
            "completion_time": completion_time
        },
        "hallway_id": {
            "time_stamp": time_stamp,
            "completion_time": completion_time
        },
        ...
    }
    "AGV_ID": {
        "hallway_id": {
            "time_stamp": time_stamp,
            "completion_time": completion_time
        },
        "hallway_id": {
            "time_stamp": time_stamp,
            "completion_time": completion_time
        },
        ...
    }
}
check time_stamp and sort the hallways based on time_stamp
execute simulation in bulk for each time_stamp, log the completion time for each AGV
for each time_stamp:
    for each hallway in time_stamp:
        execute simulation -> output: [(AGV ID, Time),...]
        for each AGV in output:
            AGV_COMPLETION_LOGS[AGV_ID][hallway_id] = {"time_stamp": time_stamp, "completion_time": completion_time}
            
"""
class BulkHallwaySimulator:
    def __init__(self):
        self.scenario_id = ""
        self.human_distribution_function = ""
        self.hallways = {}
        self.AGV_COMPLETION_LOGS = {}

    def readJson(self, json_data):
        self.scenario_id = json_data["Scenario_ID"]
        self.human_distribution_function = json_data["Human_distribution_function"]
        self.hallways = json_data["hallways"]

    def read_function(self, function):
        # y = a * x + b (x[from,to])
        """
        get a, b, from, to
        """
        self.human_distribution_function = function # distribute base on x which is time_stamp, this function to calculate the number of people in the hallway
        splitted = function.split(" ")
        self.a = splitted[2]
        self.b = splitted[4]
        self.left_bound = splitted[6].split(",")[0]
        self.right_bound = splitted[6].split(",")[1]

    def prepare_data(self):
        # check the time_stamp and create a list of time_stamp(empty json object)
        time_stamps = set()
        for hallway in self.hallways:
            time_stamps.add(hallway["time_stamp"])
        time_stamps = sorted(list(time_stamps))

        # create json object for each time_stamp
        self.run_dict = {}
        for time_stamp in time_stamps:
            self.run_dict[time_stamp] = []
            for hallway in self.hallways:
                if hallway["time_stamp"] == time_stamp:
                    self.run_dict[time_stamp].append(hallway)

        # generate variables for logging the completion time of each AGV
        # read all AGV IDs from the hallways
        agv_ids = set()
        self.AGV_COMPLETION_LOGS = {}
        for hallway in self.hallways:
            for ids in hallway["agv_ids"]:
                for agv_id in ids:
                    agv_ids.add(agv_id)
        for agv_id in agv_ids:
            self.AGV_COMPLETION_LOGS[agv_id] = {}

        # calculate the number of people in the hallway for each time_stamp and add to the hallway object
        for time_stamp in time_stamps:
            for hallway in self.run_dict[time_stamp]:
                x = time_stamp
                y = self.a * x + self.b
                hallway["num_people"] = y

    def run_simulation(self):
        self.prepare_data()
        # call class HallwaySimulator to run the simulation
        hallway_simulator = HallwaySimulator()
        for time_stamp in self.run_dict:
            for hallway in self.run_dict[time_stamp]:
                hallway_simulator.set_params(
                    hallway["hallway_id"],
                    hallway["height"],
                    hallway["width"],
                    hallway["agv_ids"],
                    hallway["agv_directions"],
                    hallway["num_people"],
                    hallway["human_type_distribution"],
                    time_stamp,
                    0
                )
                output = hallway_simulator.run_simulation()
                for agv in output:
                    self.AGV_COMPLETION_LOGS[agv[0]][hallway["hallway_id"]] = {"time_stamp": time_stamp, "completion_time": agv[1]}
        return self.AGV_COMPLETION_LOGS
    


