import gamelib
from constants import *
from misc import *

############################ HIGH LEVEL ########################################

def execute_standard_strategy(game_state, state):
    reset_state(state)
    build_defense(game_state, state)
    build_offense(game_state, state)


def reset_state(state):
    state["scramblers_built"] = 0
    state["pings_built"] = 0
    state["emps_built"] = 0


############################## DEFENSE #########################################

def build_defense(game_state, state):
    if game_state.turn_number == 0: 
        build_initial_defense(game_state)
    build_walls(game_state, state) 
    build_inner_defense_1(game_state, state)
    build_outer_defense_1(game_state)
    build_inner_defense_2(game_state, state)
    build_outer_defense_2(game_state, state)


def build_initial_defense(game_state):
    """Initial static defense."""
    filter_locations = [[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [18, 6], [10, 5], [11, 5], [12, 5], [15, 5], [16, 5], [17, 5]]
    game_state.attempt_spawn(FILTER, filter_locations)
    destructor_locations = [[12,4], [15,4]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)


def build_walls(game_state, state):
    """Basic funnel-wall defense."""
    # don't interrupt attack lol:
    if state["mode"] != ATTACK_MODE:
        wall_opening_locs = [[1,13], [26,13]]
        game_state.attempt_spawn(FILTER, wall_opening_locs)

    # build best wall according to given resources, use scramblers to fill in if needed
    budget = game_state.number_affordable(FILTER)

    # calculate walls and cost
    cheap_borders = [[0, 13], [1, 13], [2, 13], [3, 13], [4, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [5, 12], [22, 12], [4, 11], [23, 11]]
    cheap_borders_cost = get_need_to_build(game_state, FILTER, cheap_borders)
    stable_borders = [[0, 13], [1, 13], [2, 13], [3, 13], [4, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [5, 12], [22, 12], [4, 11], [23, 11]]
    stable_borders_cost = get_need_to_build(game_state, FILTER, stable_borders)

    # prefer stable ones if it's same price or cheaper
    if stable_borders_cost <= cheap_borders_cost:
        cheap_borders = stable_borders
        cheap_borders_cost = stable_borders_cost

    l_wall = [[10, 5], [9, 6], [8, 7], [7, 8], [6, 9], [5, 10]]
    l_wall_cost = get_need_to_build(game_state, FILTER, l_wall)
    r_wall = [[17, 5], [18, 6], [19, 7], [20, 8], [21, 9], [22, 10]]
    r_wall_cost = get_need_to_build(game_state, FILTER, r_wall)

    game_state.attempt_spawn(FILTER, l_wall)
    if budget < l_wall_cost:
        state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [7,6])

    game_state.attempt_spawn(FILTER, r_wall)
    if budget < l_wall_cost + r_wall_cost:
        state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [20,6])

    if budget > l_wall_cost + r_wall_cost + stable_borders_cost:
        game_state.attempt_spawn(FILTER, stable_borders)
    else:
        game_state.attempt_spawn(FILTER, cheap_borders)
    if budget < l_wall_cost + r_wall_cost + cheap_borders_cost:
        plug_borders(game_state, cheap_borders, state)

    # excess budget:
    central_destructor_shields = [[11, 5], [12, 5], [15, 5], [16, 5]]
    game_state.attempt_spawn(FILTER, central_destructor_shields)


def plug_borders(game_state, border_locs, state):
    need_to_build = get_need_to_build(game_state, FILTER, border_locs)

    # if enemy has destructor on early path, don't waste scramblers
    if need_to_build > 7:
        path = game_state.find_path_to_edge([3,10], game_state.game_map.TOP_RIGHT)
        if path is None or len(path) < 8 or not any(game_state.get_attackers(coord, 1) for coord in path[:6]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [3,10])

    if need_to_build > 0:
        path = game_state.find_path_to_edge([24,10], game_state.game_map.TOP_LEFT)
        if path is None or len(path) < 8 or not any(game_state.get_attackers(coord, 1) for coord in path[:6]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [24,10])


def build_inner_defense_1(game_state, state):
    locs = [[12,4], [15,4]]
    num_needed = get_need_to_build(game_state, DESTRUCTOR, locs)
    num_got = game_state.attempt_spawn(DESTRUCTOR, locs)
    if num_got < num_needed and state["scramblers_built"] < 4:
        if game_state.contains_stationary_unit([14,1]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [15,1])
        elif game_state.contains_stationary_unit([13,1]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [12,1])


def build_outer_defense_1(game_state):
    if game_state.get_resource(game_state.CORES) < 7:
        return
    locs = [[4,12], [23,12]]
    random.shuffle(locs)
    game_state.attempt_spawn(DESTRUCTOR, locs)


def build_inner_defense_2(game_state, state):
    if state["danger_unit"] == FILTER or game_state.get_resource(game_state.CORES > 46):
        #locs = [[15,3], [12,3]]
        locs = [[15,3], [12,3], [16,4], [11,4], [11,3], [16,3]]
        random.shuffle(locs)
        for loc in locs:
            replace_unit(game_state, loc, FILTER, DESTRUCTOR)
        ################ MAYBE DELETE THIS? >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        locs = [[11,6], [12,6], [15,6], [16,6]]
        game_state.attempt_spawn(FILTER, locs)
        for loc in locs:
            replace_unit(game_state, loc, FILTER, DESTRUCTOR)
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  MAYBE DELETE THIS? ################
    else:
        pass


def build_outer_defense_2(game_state, state):
    if state["danger_unit"] == FILTER:
        pass
    elif state["danger_unit"] == EMP or game_state.get_resource(game_state.CORES > 46):
        #locs = [[3,12], [24,12]]
        locs = [[3,12], [24,12], [2,12], [25,12], [1,12], [26,12]] 
        random.shuffle(locs)
        for loc in locs:
            replace_unit(game_state, loc, FILTER, DESTRUCTOR)


def build_inner_defense_3(game_state, state):
    """unused"""
    if game_state.get_resource(game_state.CORES) > 40:
        if state["danger_unit"] == FILTER:
            pass
        elif state["danger_unit"] == EMP:
            pass

def build_outer_defense_3(game_state, state):
    """unused"""
    if game_state.get_resource(game_state.CORES) > 40:
        if state["danger_unit"] == FILTER:
            pass
        elif state["danger_unit"] == EMP:
            pass



########################### BUILD OFFENSE ######################################
def build_offense(game_state, state):
    #game_state.attempt_spawn(ENCRYPTOR, [[13,0], [14,0]]) 
    #if game_state.get_resource(game_state.BITS) > 16 + game_state.turn_number / 8:
    #    game_state.attempt_spawn(PING, random.sample([[12,1], [15,1]], 1), num=50)
    if game_state.get_resource(game_state.CORES) > 20:
        locs = [[10, 4], [17, 4], [10, 3], [17, 3], [11, 2], [12, 2], [15, 2], [16, 2], [12, 1], [15, 1]]
        random.shuffle(locs)
        game_state.attempt_spawn(ENCRYPTOR, locs)
    if game_state.get_resource(game_state.BITS) > 16 + game_state.turn_number / 8:
        game_state.attempt_spawn(PING, random.sample([[13,0], [14,0]], 1), num=50)

