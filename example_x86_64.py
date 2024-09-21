from x86_64.hallway_simulator_module.HallwaySimulator import HallwaySimulator
import os

hallway_simulator = HallwaySimulator()
"""
self.hallway_id = 0 # string
self.hallway_length = 0 # int
self.hallway_width = 0 # int
self.agv_ids = [] # list of int
self.agv_directions = [] # list of int
self.num_people = 0 # int
self.human_type_distribution = [] # list of int
self.time_stamp = 0 # int
self.event_type = 0 # int
"""
os.system("pwd")
hallway_simulator.set_params("hallway_1", 66, 4, [0,1], [0,1], 0, [22, 5, 17, 22, 17, 17], 0, 0)
output = hallway_simulator.run_simulation()
print(output) # [(AGV ID, Time),...]
