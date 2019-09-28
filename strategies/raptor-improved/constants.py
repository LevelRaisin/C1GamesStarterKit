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

# game_map opponent's regions (list of locations):
L_WING = [[6, 16], [6, 17], [6, 18], [7, 15], [7, 16], [7, 17], [7, 18], [7, 19], [8, 14], [8, 15], [8, 16], [8, 17], [8, 18], [8, 19], [8, 20], [9, 14], [9, 15], [9, 16], [9, 17], [9, 18], [9, 19], [9, 20], [10, 14], [10, 15], [10, 16], [10, 17], [10, 18], [10, 19], [10, 20], [11, 15], [11, 16], [11, 17], [11, 18], [11, 19], [12, 16], [12, 17], [12, 18]]
L_CENTRAL = [[9, 16], [9, 17], [9, 18], [9, 19], [9, 20], [10, 15], [10, 16], [10, 17], [10, 18], [10, 19], [10, 20], [10, 21], [11, 14], [11, 15], [11, 16], [11, 17], [11, 18], [11, 19], [11, 20], [11, 21], [11, 22], [12, 14], [12, 15], [12, 16], [12, 17], [12, 18], [12, 19], [12, 20], [12, 21], [12, 22], [13, 14], [13, 15], [13, 16], [13, 17], [13, 18], [13, 19], [13, 20], [13, 21], [13, 22], [14, 14], [14, 15], [14, 16], [14, 17], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [15, 14], [15, 15], [15, 16], [15, 17], [15, 18], [15, 19], [15, 20], [15, 21], [15, 22], [16, 15], [16, 16], [16, 17], [16, 18], [16, 19], [16, 20], [16, 21], [17, 16], [17, 17], [17, 18], [17, 19], [17, 20]]
L_PIT = [[8, 20], [8, 21], [8, 22], [9, 19], [9, 20], [9, 21], [9, 22], [9, 23], [10, 18], [10, 19], [10, 20], [10, 21], [10, 22], [10, 23], [10, 24], [11, 18], [11, 19], [11, 20], [11, 21], [11, 22], [11, 23], [11, 24], [11, 25], [12, 18], [12, 19], [12, 20], [12, 21], [12, 22], [12, 23], [12, 24], [12, 25], [12, 26], [13, 18], [13, 19], [13, 20], [13, 21], [13, 22], [13, 23], [13, 24], [13, 25], [13, 26], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [14, 23], [14, 24], [14, 25], [14, 26], [15, 19], [15, 20], [15, 21], [15, 22], [15, 23], [15, 24], [15, 25], [16, 20], [16, 21], [16, 22], [16, 23], [16, 24]]
L_CORNER = [[2, 15], [2, 16], [3, 14], [3, 15], [3, 16], [3, 17], [4, 14], [4, 15], [4, 16], [4, 17], [4, 18], [5, 14], [5, 15], [5, 16], [5, 17], [5, 18], [6, 15], [6, 16], [6, 17]]
L_CORNER_TIP = [[0, 13], [0, 14], [1, 12], [1, 13], [1, 14], [1, 15], [2, 12], [2, 13], [2, 14], [2, 15], [2, 16], [3, 12], [3, 13], [3, 14], [3, 15], [3, 16], [4, 13], [4, 14], [4, 15]]

R_WING = [[15, 16], [15, 17], [15, 18], [16, 15], [16, 16], [16, 17], [16, 18], [16, 19], [17, 14], [17, 15], [17, 16], [17, 17], [17, 18], [17, 19], [17, 20], [18, 14], [18, 15], [18, 16], [18, 17], [18, 18], [18, 19], [18, 20], [19, 14], [19, 15], [19, 16], [19, 17], [19, 18], [19, 19], [19, 20], [20, 15], [20, 16], [20, 17], [20, 18], [20, 19], [21, 16], [21, 17], [21, 18]]
R_CENTRAL = [[10, 16], [10, 17], [10, 18], [10, 19], [10, 20], [11, 15], [11, 16], [11, 17], [11, 18], [11, 19], [11, 20], [11, 21], [12, 14], [12, 15], [12, 16], [12, 17], [12, 18], [12, 19], [12, 20], [12, 21], [12, 22], [13, 14], [13, 15], [13, 16], [13, 17], [13, 18], [13, 19], [13, 20], [13, 21], [13, 22], [14, 14], [14, 15], [14, 16], [14, 17], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [15, 14], [15, 15], [15, 16], [15, 17], [15, 18], [15, 19], [15, 20], [15, 21], [15, 22], [16, 14], [16, 15], [16, 16], [16, 17], [16, 18], [16, 19], [16, 20], [16, 21], [16, 22], [17, 15], [17, 16], [17, 17], [17, 18], [17, 19], [17, 20], [17, 21], [18, 16], [18, 17], [18, 18], [18, 19], [18, 20]]
R_PIT = [[11, 20], [11, 21], [11, 22], [11, 23], [11, 24], [12, 19], [12, 20], [12, 21], [12, 22], [12, 23], [12, 24], [12, 25], [13, 18], [13, 19], [13, 20], [13, 21], [13, 22], [13, 23], [13, 24], [13, 25], [13, 26], [14, 18], [14, 19], [14, 20], [14, 21], [14, 22], [14, 23], [14, 24], [14, 25], [14, 26], [15, 18], [15, 19], [15, 20], [15, 21], [15, 22], [15, 23], [15, 24], [15, 25], [15, 26], [16, 18], [16, 19], [16, 20], [16, 21], [16, 22], [16, 23], [16, 24], [16, 25], [17, 18], [17, 19], [17, 20], [17, 21], [17, 22], [17, 23], [17, 24], [18, 19], [18, 20], [18, 21], [18, 22], [18, 23], [19, 20], [19, 21], [19, 22]]
R_CORNER = [[21, 15], [21, 16], [21, 17], [22, 14], [22, 15], [22, 16], [22, 17], [22, 18], [23, 14], [23, 15], [23, 16], [23, 17], [23, 18], [24, 14], [24, 15], [24, 16], [24, 17], [25, 15], [25, 16]]
R_CORNER_TIP = [[23, 13], [23, 14], [23, 15], [24, 12], [24, 13], [24, 14], [24, 15], [24, 16], [25, 12], [25, 13], [25, 14], [25, 15], [25, 16], [26, 12], [26, 13], [26, 14], [26, 15], [27, 13], [27, 14]]

PIT_AREA = [[15, 20], [17, 20], [18, 19], [9, 21], [14, 18], [11, 22], [10, 18], [16, 22], [17, 23], [16, 25], [13, 20], [18, 20], [8, 21], [14, 24], [10, 24], [11, 21], [10, 23], [16, 19], [12, 22], [17, 18], [13, 23], [14, 21], [9, 19], [13, 26], [15, 26], [14, 22], [15, 23], [12, 24], [17, 24], [9, 20], [15, 25], [14, 19], [10, 19], [16, 23], [12, 18], [17, 22], [13, 19], [18, 21], [8, 22], [14, 25], [9, 23], [11, 20], [10, 20], [16, 20], [12, 23], [11, 25], [13, 22], [18, 22], [14, 26], [19, 22], [15, 19], [11, 19], [12, 20], [13, 25], [14, 23], [19, 21], [15, 22], [12, 25], [15, 24], [15, 21], [12, 19], [17, 21], [13, 18], [9, 22], [11, 23], [10, 21], [16, 21], [11, 24], [16, 24], [13, 21], [18, 23], [8, 20], [15, 18], [11, 18], [10, 22], [16, 18], [12, 21], [17, 19], [13, 24], [14, 20], [19, 20], [12, 26]]
CENTRAL_AREA = [[14, 17], [19, 19], [10, 17], [15, 20], [17, 20], [13, 17], [18, 19], [14, 18], [11, 22], [10, 18], [19, 14], [7, 19], [16, 22], [12, 17], [13, 20], [18, 20], [8, 15], [9, 14], [9, 16], [14, 15], [20, 19], [11, 21], [15, 14], [16, 19], [21, 18], [12, 22], [17, 18], [10, 14], [8, 18], [14, 21], [11, 15], [9, 19], [15, 16], [6, 16], [20, 16], [11, 16], [16, 16], [18, 15], [14, 22], [19, 18], [7, 15], [13, 16], [18, 16], [9, 20], [14, 19], [19, 17], [10, 19], [7, 18], [12, 18], [13, 19], [11, 20], [10, 20], [7, 17], [16, 20], [21, 17], [20, 15], [17, 17], [13, 22], [10, 15], [8, 19], [11, 14], [9, 18], [15, 19], [6, 17], [16, 14], [20, 17], [11, 19], [17, 15], [16, 17], [12, 20], [8, 16], [15, 22], [6, 18], [12, 14], [13, 15], [18, 17], [14, 16], [19, 16], [10, 16], [15, 21], [12, 19], [17, 21], [13, 18], [18, 18], [19, 15], [10, 21], [7, 16], [16, 21], [21, 16], [12, 16], [17, 16], [13, 21], [8, 14], [9, 15], [8, 20], [9, 17], [15, 18], [14, 14], [16, 15], [20, 18], [11, 18], [17, 14], [15, 15], [16, 18], [12, 21], [17, 19], [8, 17], [14, 20], [19, 20], [15, 17], [12, 15], [11, 17], [13, 14], [18, 14]]
CORNER_AREA = [[3, 15], [25, 16], [26, 14], [24, 17], [4, 18], [0, 14], [25, 12], [1, 15], [24, 13], [2, 12], [21, 16], [6, 17], [3, 17], [3, 14], [26, 15], [27, 14], [23, 17], [5, 18], [1, 14], [22, 16], [22, 14], [4, 13], [24, 14], [2, 13], [23, 15], [25, 15], [3, 16], [6, 15], [26, 12], [2, 16], [23, 16], [3, 13], [5, 17], [1, 13], [22, 17], [22, 15], [4, 14], [24, 15], [4, 16], [27, 13], [23, 14], [5, 15], [25, 14], [26, 13], [2, 14], [21, 15], [3, 12], [5, 16], [1, 12], [4, 15], [24, 16], [4, 17], [0, 13], [5, 14], [25, 13], [22, 18], [24, 12], [2, 15], [21, 17], [23, 13], [6, 16], [23, 18]]

# opponent defensive types:
RAPTOR = "RAP"
SMILE = "SML"
CENTRAL = "CTL"
POLE = "PL"
CORNER = "CRN"
PIT = "PIT"
NO_DEFENSE = "NOD"
BALANCE = "BAL"

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

