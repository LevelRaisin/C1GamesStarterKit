# EMP attack hole locations:
#HOLES = [
#    [[1,13], [26,13]],
#    [[1,13], [26,13]],
#    [[5,10], [22,10]],
#]
HOLES = [
    [[5,10], [22,10]],
    [[1,13], [26,13]],
]

# game_map directions:
TOP_RIGHT = 0
TOP_LEFT = 1

# unit types. the strings will be overloaded with rich object data once algo starts:
FILTER = "FF"
ENCRYPTOR = "EF"
DESTRUCTOR = "DF"
PING = "PI"
EMP = "EI"
SCRAMBLER = "SI"
UNIT_TYPES = {
    FILTER: None,
    ENCRYPTOR: None,
    DESTRUCTOR: None,
    PING: None,
    EMP: None,
    SCRAMBLER: None,
}

# standard strategy's EMP attack status
UNLOADED = 0
READY_TO_FIRE = 1

# map locations
ENEMY_LOCATIONS = []
for row in range(14):
    y_index = 27 - row
    x_lower_bound = 13 - row
    x_upper_bound = 14 + row
    for x_index in range(x_lower_bound, x_upper_bound + 1):
        ENEMY_LOCATIONS.append([x_index, y_index])

PLAYER_LOCATIONS = []
for row in range(14):
    y_index = row
    x_lower_bound = 13 - row
    x_upper_bound = 14 + row
    for x_index in range(x_lower_bound, x_upper_bound + 1):
        PLAYER_LOCATIONS.append([x_index, y_index])

# WALL LOCATIONS:
CHEAP_BORDERS = set([(0, 13), (1, 13), (2, 13), (3, 13), (4, 13), (23, 13), (24, 13), (25, 13), (26, 13), (27, 13), (5, 12), (22, 12), (4, 11), (23, 11)])
STABLE_BORDERS = set([(0, 13), (1, 13), (2, 13), (3, 13), (4, 13), (23, 13), (24, 13), (25, 13), (26, 13),  (27, 13), (5, 12), (22, 12), (4, 11), (23, 11)])
L_WALL = set([(10, 5), (9, 6), (8, 7), (7, 8), (6, 9), (5, 10)])
R_WALL = set([(17, 5), (18, 6), (19, 7), (20, 8), (21, 9), (22, 10)])

# hit_map region names
MAP_REGIONS = ["inner", "outerL", "outerR", "wallL", "wallR"]

