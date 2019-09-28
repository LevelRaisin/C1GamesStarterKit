from functools import partial
import math
import copy
import gamelib
from constants import *
from misc import *

############################ HIGH LEVEL ########################################

def execute_standard_strategy(game_state, state):
    reset_state(game_state, state)
    build_defense(game_state, state)
    build_offense(game_state, state)


def reset_state(game_state, state):
    pass


############################## DEFENSE #########################################

def build_defense(game_state, state):
    if game_state.turn_number == 0: 
        build_initial_defense(game_state)
    build_walls(game_state, state) 
    build_inner_defense_1(game_state, state)
    build_outer_defense_1(game_state)
    delete_weak_prominent_filters(game_state, state)
    build_encryptors_with_excess_cores(game_state, state)


def build_initial_defense(game_state):
    """Initial static defense."""
    destructor_locations = [[1, 12], [2, 12], [25, 12], [26, 12], [11, 7], [16, 7], [12, 6], [13, 6], [14, 6], [15, 6]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)
    filter_locations = [[13,7], [14,7], [1, 13], [3, 13], [24, 13], [26, 13], [5, 11], [22, 11], [7, 9], [20, 9], [10, 8], [11, 8], [12, 8], [15, 8], [16, 8], [17, 8]]
    game_state.attempt_spawn(FILTER, filter_locations)


def delete_weak_walls(game_state, state):
    pass
#    cores_needed = 0
#    num_cores = game_state.get_resource(game_state.CORES)
#    if num_cores == 0: # used up all cores to build defense
#        return False
#
#    l_wall = [[10, 5], [9, 6], [8, 7], [7, 8], [6, 9], [5, 10]]
#    r_wall = [[17, 5], [18, 6], [19, 7], [20, 8], [21, 9], [22, 10]]
#    stable_borders = [[0, 13], [2, 13], [3, 13], [4, 13], [23, 13], [24, 13], [25, 13], [27, 13], [5, 12], [22, 12], [4, 11], [23, 11]]
#    wall_locs = l_wall + r_wall + stable_borders
#    tiles = filter(lambda _: _, get_tiles(game_state, wall_locs)) # filter out missing walls
#    tiles = [tile[0] for tile in tiles] # retrieve singular stationary unit
#
#    # EDIT: we don't need this snippet here; if num_cores > 0, means we finished building our defense, and have some cores to spare.
#      # cores_needed += len(wall_locs) - len(tiles)
#
#    weak_tiles = list(filter(lambda tile: tile.stability <= 10, tiles))
#    weak_tiles.sort(key=lambda tile: tile.stability)
#
#    tiles_to_fix = weak_tiles[:int(num_cores)]
#    coords = [[tile.x, tile.y] for tile in tiles_to_fix]
#
#    if coords:
#        game_state.attempt_remove(coords)
#    return True


def build_walls(game_state, state):
    """Basic funnel-wall defense."""

    encryptor_locations = [[0, 13], [2, 13], [25, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [7, 8], [8, 8], [9, 8], [18, 8], [19, 8], [20, 8]]
    # don't interrupt attack lol:
    holes = []
    if state["ping_attack_prepared"]:
        # TODO: sub with get_loc later
        holes = [[6,9], [21,9]]
    for hole in holes:
        encryptor_locations.remove(hole)
    game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)

    missing_locs = list(filter(lambda loc: not game_state.game_map[loc], encryptor_locations))
    if len(missing_locs) == 0: return True
    location_dict = dict(encryptor_locations)
    xs = [loc[0] for loc in missing_locs]
    xs.sort()

    # build scramblers:
    index = 0
    for i in range(4):
        upper_bound = 7 * (i+1)
        avg_x = count = 0
        while index < len(xs) and xs[index] < upper_bound:
            avg_x += xs[index]
            count += 1
            index += 1
        if count > 0:
            # find average point to spawn scrambler:
            avg_x = int(avg_x / count)
            avg_x = int(avg_x / count)
            if avg_x not in location_dict: continue
            avg_y = location_dict[avg_x]

            # find spawn point
            nearest_edge = game_state.game_map.BOTTOM_LEFT if i < 2 else game_state.game_map.BOTTOM_RIGHT
            path = game_state.find_path_to_edge([avg_x, avg_y], nearest_edge)
            if not path or not is_edge(path[-1]): continue

            # abort if the scrambler would get stuck
            spawn_point = path[-1]
            opposite_edge = game_state.game_map.TOP_RIGHT if i < 2 else game_state.game_map.TOP_LEFT 
            path = game_state.find_path_to_edge(spawn_point, opposite_edge)
            if not path or len(path) < 20: continue

            # generate scrambler:
            game_state.attempt_spawn(SCRAMBLER, spawn_point)

    filter_locations = [[13,7], [14,7], [1, 13], [3, 13], [24, 13], [26, 13], [5, 11], [22, 11], [7, 9], [20, 9], [10, 8], [11, 8], [12, 8], [15, 8], [16, 8], [17, 8]]
    game_state.attempt_spawn(FILTER, filter_locations)


def build_inner_defense_1(game_state, state):
    locs = [[12,7], [15,7]]
    game_state.attempt_spawn(DESTRUCTOR, locs)
    num_destructors_made = int(bool(game_state.game_map[12,7])) + int(bool(game_state.game_map[15,7]))
    enemy_pings = game_state.get_resource(game_state.BITS, 1) - 9
    scramblers_needed = int(enemy_pings / 6)
    if num_destructors_made < 2: scramblers_needed += 1
    game_state.attempt_spawn(SCRAMBLER, [18,4], num=min(4, scramblers_needed)) 


def build_outer_defense_1(game_state):
    locs = [[2,12], [23,12], [24,12]]
    game_state.attempt_spawn(DESTRUCTOR, locs)


########################### BUILD OFFENSE ######################################
def build_offense(game_state, state):
    if state["ping_attack_prepared"]:
        attack = state["ping_attack_prepared"]
        order = [True, False]
        random.shuffle(order)
        success = launch_ping_attack(game_state, state, attack, r = order[0])
        if success: return
        success = launch_ping_attack(game_state, state, attack, r = order[1])
        if success: return
        brute_ping(game_state, state)
        state["ping_attack_prepared"] = None
    else:
        tn = game_state.turn_number
        #         EMP,  PING
        attack = [2, 6]
        attack = [2, 14]
        attack = [3, 16]
        if tn > 10: attack = [2, 10]
        elif tn > 20: attack = [2, 10]
        elif tn > 30: attack = [2, 14]
        elif tn > 40: attack = [3, 16]

        n_emps, n_pings = attack
        n_pings = min(n_pings, game_state.enemy_health + 5)
        cost = n_emps * 3 + n_pings
        if game_state.project_future_bits(1, 0) >= cost:
            prepare_ping_attack(game_state, state)
            state["ping_attack_prepared"] = attack


def prepare_ping_attack(game_state, state):
    holes = [get_loc([6,9], True), get_loc([6,9], False)]
    game_state.attempt_remove(holes)


def launch_ping_attack(game_state, state, attack, r): # -> bool, True if attack was launched, False otherwise
    hole = get_loc([6,9], r) 
    ping_spawn_point = get_loc([23,9], r)
    emp_spawn_point = get_loc([24,10], r)
    edge = TOP_RIGHT if r else TOP_LEFT

    path = game_state.find_path_to_edge(ping_spawn_point, edge)
    #if hole not in path: return False # TODO enable or not?

    n_emps, n_pings = attack
    game_state.attempt_spawn(EMP, emp_spawn_point, num=n_emps)
    game_state.attempt_spawn(PING, ping_spawn_point, num=n_pings)


def build_encryptors_with_excess_cores(game_state, state):
    locs = [[9, 6], [10, 6], [17, 6], [18, 6], [10, 5], [11, 5], [16, 5], [17, 5]] + [[11, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4], [12, 3], [13, 3], [14, 3], [15, 3]] + [[12, 1], [13, 1], [14, 1], [15, 1], [13, 0], [14, 0]]
    empty_locs = [loc for loc in locs if not game_state.game_map[loc]]

    current_encryptors = len(locs) - len(empty_locs)
    can_build = int((game_state.get_resource(game_state.CORES) - 20))
    ping_hp = 15 + 3 * (current_encryptors + can_build)
    optimal_ping_hp = ping_hp - (ping_hp % 8) + 1
    n = int((optimal_ping_hp - 15) / 3) - current_encryptors
    assert(n <= can_build)

    to_build = empty_locs[:n]
    game_state.attempt_spawn(ENCRYPTOR, to_build)

