from hallway_simulator_module.HallwaySimulator import HallwaySimulator, BulkHallwaySimulator, clean_up

clean_up()

def getReal_preprocess(Map_file, function_file):
    # read 2 files Map_file(txt) and function_file(txt)
    """
    Map_file: a <src> <dest> <low> <cap> <cost> <hallway_id> <human_distribution_percentage>
    if src < dest: left to right
    if src > dest: right to left
    a 1 2 0 1 1 Region_1 3
    a 3 2 0 1 1 Region_1 4
    a 1 4 0 1 1 Region_2 5
    a 5 4 0 1 1 Region_2 3
    ...
    """
    """
    function_file: each line
    y = 34 * x + 32 (0,50)
    y = 3 * x + -100 (60,500)
    """
    # read files
    map_data = None
    function_data = None
    with open(Map_file, 'r', encoding='utf-8') as file:
        map_data = file.readlines()
    with open(function_file, 'r', encoding='utf-8') as file:
        function_data = file.readlines()
    # process data
    """
    hallways_list = [
        {
            "hallway_id": "Region_1",
            "length": 66, # change base on cost * 0.6
            "width": 4, # constant default to 4
            "agents_distribution": 15
        },
        {
            "hallway_id": "Region_2",
            "length": 66, # change base on cost * 0.6
            "width": 4, # constant
            "agents_distribution": 12
        }
    ]
    """
    """
    functions_list = [
        "y = 34 * x + 32 (0,50)",
        "y = 3 * x + -100 (60,500)"
    ]
    """
    hallways_list = []
    functions_list = []
    for line in map_data:
        line = line.strip()
        parts = line.split(" ")
        if len(parts) == 8:
            hallway = {
                "hallway_id": parts[6],
                "length": int(int(parts[5]) * 0.6),
                "width": 4,
                "agents_distribution": int(parts[7]),
                "src": int(parts[1]),
                "dest": int(parts[2])
            }
            hallways_list.append(hallway)
    for line in function_data:
        line = line.strip()
        functions_list.append(line)
    return hallways_list, functions_list


def getReal_V2(Map_file, function_file, start_id, next_id, agv, current_time):
    hallways_list, functions_list = getReal_preprocess(Map_file, function_file)
    events_list = []  # actually only has one event but because of the structure of the code, it has to be a list
    """
    {
        "AgvIDs": [0], # depends
        "AgvDirections": [0], # depends
        "time_stamp": 0, # depends
        "hallway_id": "hallway_1" # depends
    }
    """
    # get the agv id from the agv object id: AGV1 -> 1
    agv_id = int(agv.id[3:])
    # get the direction of the agv by querying the hallways_list with the start_id and next_id
    direction = 0
    for hallway in hallways_list:
        if hallway["src"] == start_id and hallway["dest"] == next_id:
            direction = 1
            hallway_id = hallway["hallway_id"]
            break
        if hallway["src"] == next_id and hallway["dest"] == start_id:
            direction = -1
            hallway_id = hallway["hallway_id"]
            break
    # get the time_stamp from the current_time
    time_stamp = current_time

    # add to json
    event = {
        "AgvIDs": [agv_id],
        "AgvDirections": [direction],
        "time_stamp": time_stamp,
        "hallway_id": hallway_id
    }
    events_list.append(event)

    # filter the hallways_list to only have the hallway that the agv is currently in
    hallways_list = [hallway for hallway in hallways_list if event["hallway_id"] == hallway_id and (hallway["src"] - hallway["dest"]) * direction > 0]

    print(hallways_list)
    print(functions_list)
    print(events_list)

    bulk_sim = BulkHallwaySimulator("test", 800, hallways_list, functions_list, events_list)
    result = bulk_sim.run_simulation()
    # result will look like this: {0: {'hallway_1': {'time_stamp': 0, 'completion_time': 111}}, 1: {'hallway_1': {'time_stamp': 0, 'completion_time': 111}}}
    # get the completion_time from the result
    completion_time = result[agv_id][hallway_id]["completion_time"]
    return completion_time

class AGV:
    def __init__(self, id):
        self.id = id


map_file = "output.txt"
function_file = "functions.txt"
start_id = 3
next_id = 2
agv = AGV("AGV1")
current_time = 0
print(getReal_V2(map_file, function_file, start_id, next_id, agv, current_time))