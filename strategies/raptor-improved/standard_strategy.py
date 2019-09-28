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
    determine_emp_strategy(game_state, state)
    if game_state.turn_number == 0: 
        build_initial_defense(game_state)
    build_walls(game_state, state) 
    build_inner_defense_1(game_state, state)
    build_outer_defense_1(game_state)
    delete_weak_walls(game_state, state)
    
    real_reserve = set_reserve(game_state, 12)
    build_reinforcing_destructors(game_state, state)
    build_encryptors(game_state, state)
    unset_reserve(game_state, real_reserve)


def build_initial_defense(game_state):
    """Initial static defense."""
    filter_locations = [[0, 13], [1, 13], [2, 13], [23, 13], [24, 13], [25, 13], [26, 13], [27, 13], [3, 12], [22, 12], [4, 11], [22, 11], [5, 10], [6, 10], [21, 10], [7, 9], [8, 9], [19, 9], [20, 9], [9, 8], [10, 8], [11, 8], [12, 8], [15, 8], [16, 8], [17, 8], [18, 8]]
    game_state.attempt_spawn(FILTER, filter_locations)
    destructor_locations = [[12, 7], [15, 7]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)


def determine_emp_strategy(game_state, state):
    if units_at(game_state, [[8, 20], [7, 19], [6, 18], [5, 17]]):
        state["hole"] = [[26,13]]
    else:
        state["hole"] = [[26,13], [26,13], [22,11]]


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
    # don't interrupt attack lol:
    hole = get_hole(state)
    filter_locations = state["walls"]
    if state["is_emp_attacking"]: filter_locations.remove(hole)
    game_state.attempt_spawn(FILTER, filter_locations)
    if state["is_emp_attacking"]: filter_locations.append(hole)

    missing_locs = list(filter(lambda loc: not game_state.game_map[loc], filter_locations))
    if len(missing_locs) == 0: return True
    location_dict = dict(filter_locations)
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


def build_reinforcing_destructors(game_state, state):
    saved = set_budget(game_state, 10)
    if game_state.get_resource(game_state.CORES) < 7:
        return False

    filter_locs = [[20,10], [4,12], [5,11], [11,9], [12,9], [15,9], [16,9]] # [21,11] need to leave blank for emp attack
    destructor_locs = [[1,12], [13,6], [12,8], [15,8], [23,11], [16,8], [11,8], [2,11], [22,12]] 

    if "walls_updated" not in state:
        walls = (set(tuple(l) for l in state["walls"]) - set(tuple(l) for l in destructor_locs)) | set(tuple(l) for l in filter_locs)
        state["walls"] = [list(t) for t in walls]
        state["walls_updated"] = True

    game_state.attempt_spawn(FILTER, filter_locs)
    for d_loc in destructor_locs:
        replace_and_update_wall(game_state, state, d_loc, FILTER, DESTRUCTOR)

    unset_budget(game_state, saved)


def build_encryptors(game_state, state):
    saved = set_budget(game_state, 8)
    encryptor_locs = [[12,6], [13,5], [14,5], [15,5], [16,5], [17,5], [19, 7], [19, 6], [19, 5], [19, 8], [20, 8], [20, 7], [21, 7], [20, 6]]
    encryptor_locs += [[16, 4], [13, 3], [14, 3], [15, 2], [16, 2], [15, 1], [11, 4], [12, 3], [12, 1], [13, 1]]
    encryptor_locs += [[8, 7], [9, 7], [10, 7], [11, 7], [16, 7], [17, 7], [18, 7], [7, 6], [8, 6], [9, 6], [10, 6], [11, 6], [8, 5], [9, 5], [9, 4]]
    game_state.attempt_spawn(ENCRYPTOR, encryptor_locs)
    unset_budget(game_state, saved)




########################### BUILD OFFENSE ######################################
def execute_one_of(fns, *args):
    for fn in fns:
        if fn(*args): #.result
            return True
    return False


def build_offense(game_state, state):
    tn = game_state.turn_number
    #         EMP,  PING
    attack = [2, 6]
    attack = [2, 14]
    attack = [3, 16]
    if tn > 10: attack = [2, 10]
    elif tn > 20: attack = [2, 10]
    elif tn > 30: attack = [2, 14]
    elif tn > 40: attack = [3, 16]
    ping_attacked = launch_ping_attack(game_state, state)

    #hole = get_hole(state)
    #if hole == [22,11]:
    #    path = [[22,8], [22,9], [22,10], [22,11], [21,11], [21,12], [20,12], [20,13], [19,13], [19,14], [18,14], [18,15], [17,15]]
    #else:
    #    path = [[22,8], [22,9], [23,9], [23,10], [24,10], [24,11], [25,11], [25,12], [26,12], [26,13], [26,14], [25,14], [25,15], [24,15], [24,16]]
    #max_emp = int(game_state.project_future_bits(6, 0) / 3)
    #for emps_required in range(3, max_emp + 1):
    #    num_emp = emps_required
    #    last_step_area = set()
    #    hits_needed_to_clear = 0
    #    for step in path:
    #        curr_step_area = set(tuple(l) for l in game_state.game_map.get_locations_in_range(step, 4.5))
    #        new_area = curr_step_area - last_step_area

    #        tiles = get_tiles(game_state, list(list(t) for t in new_area))
    #        units = (tile[0] for tile in tiles if tile)
    #        enemies = filter(lambda unit: unit.player_index == 1, units)
    #        num_destructors = len(list(filter(lambda unit: unit.unit_type == DESTRUCTOR, enemies)))

    #        hits_needed_to_clear += sum(math.ceil(unit.stability / 8) for unit in units if unit.player_index == 1)
    #        hits_available = 2 * num_emp
    #        if hits_available < hits_needed_to_clear and num_destructors > 0:
    #            num_emp -= 1
    #        hits_needed_to_clear = max(hits_needed_to_clear - hits_available, 0)
    #        if num_emp <= 0: break
    #        last_step_area = curr_step_area
    #    if num_emp > 0:
    #        break
    #if emps_required < max_emp and random.random() < 0.5: emps_required += 1
    #prepare_emp_attack(game_state, state, emps_required)


def launch_ping_attack(game_state, state): # -> bool, True if attack was launched, False otherwise
    # calculate paths
    to_right_spawn = [13,0]
    to_left_spawn = [14,0]
    to_right_path = game_state.find_path_to_edge(to_right_spawn, TOP_RIGHT)
    to_left_path = game_state.find_path_to_edge(to_left_spawn, TOP_LEFT)

    # how many destructor hits do we suffer on each path?
    to_right_hits = get_damage_in_path(game_state, to_right_path)
    to_left_hits = get_damage_in_path(game_state, to_left_path)

    # calculate enemy's most vulnerable path:
    best_spawn = to_right_spawn if to_right_hits < to_left_hits else to_left_spawn
    if random.random() < 0.2: best_spawn = to_right_spawn if to_right_hits >= to_left_hits else to_left_spawn # flip 20% of the time to fuck with enemy, yafeel?
    least_hits = min(to_right_hits, to_left_hits)

    # calculate ROI
    num_pings = game_state.number_affordable(PING)
    num_encryptors = len(state["player_units"][ENCRYPTOR]) 
    if game_state.can_spawn(ENCRYPTOR, [15,1]): num_encryptors += 1
    hp_per_ping = 15 + num_encryptors * 3
    hits_per_ping = math.ceil(hp_per_ping / 16)
    potential_damage = num_pings - int(least_hits / hits_per_ping)
    gamelib.debug_write(f"Preparing ping attack: num_pings={num_pings}, expected damage: {potential_damage}.")
    if potential_damage > 8:
        game_state.attempt_spawn(ENCRYPTOR, [[15,1]])
        game_state.attempt_spawn(PING, [best_spawn], num=num_pings)
        gamelib.debug_write(f"Launching ping attack with {num_pings} pings, expected damage: {potential_damage}")
        return True
    return False

