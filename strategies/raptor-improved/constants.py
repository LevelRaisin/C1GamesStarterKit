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
