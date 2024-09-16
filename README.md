# hallway-simulator

## How to use the simulator

```python
from x86_64.hallway_simulator_module.HallwaySimulator import HallwaySimulator # for x86_64
from arm64.hallway_simulator_module.HallwaySimulator import HallwaySimulator # for arm64

"""
hallway_id = "hallway_1" # string
hallway_length = 3 # int
self.hallway_width = 6 # int
self.agv_ids = [0] # list of int
self.agv_directions = [0] # list of int
self.num_people = 50 # int
self.human_type_distribution = [22, 5, 17, 22, 17, 17] # list of int
self.time_stamp = 0 # int
self.event_type = 0 # int
"""

hallway_simulator.set_params("hallway_1", 3, 6, [0], [0], 50, [22, 5, 17, 22, 17, 17], 0, 0)
output = hallway_simulator.run_simulation() # a list of (AGV ID, Time): [(AGV ID, Time), ...]
```