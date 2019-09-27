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
    build_defense_2(game_state, state)


def reset_state(game_state, state):
    pass


############################## DEFENSE #########################################

def build_defense(game_state, state):
    if game_state.turn_number == 0: 
        build_initial_defense(game_state)
    build_walls(game_state, state) 
    build_inner_defense_1(game_state, state)
    build_outer_defense_1(game_state)
    delete_weak_walls(game_state, state)
    build_inner_defense_2(game_state, state)
    build_outer_defense_2(game_state, state)
    build_strong_defense(game_state, state)


def build_initial_defense(game_state):
    """Initial static defense."""
    filter_locations = [[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [3, 12], [24, 12], [4, 11], [23, 11], [5, 10], [22, 10], [6, 9], [21, 9], [7, 8], [20, 8], [8, 7], [19, 7], [9, 6], [18, 6], [10, 5], [11, 5], [12, 5], [15, 5], [16, 5], [17, 5]]
    game_state.attempt_spawn(FILTER, filter_locations)
    destructor_locations = [[12,4], [15,4]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)


def determine_emp_strategy(game_state, state):
    if units_at(game_state, [[8, 20], [7, 19], [6, 18], [5, 17]]):
        state["holes"] = [
            [[1,13], [26,13]]
        ]
    else:
        state["holes"] = [
            [[1,13], [26,13]],
            [[5,10], [22,10]],
            [[1,13], [26,13]],
        ]


def delete_weak_walls(game_state, state):
    cores_needed = 0
    num_cores = game_state.get_resource(game_state.CORES)
    if num_cores == 0: # used up all cores to build defense
        return False

    l_wall = [[10, 5], [9, 6], [8, 7], [7, 8], [6, 9], [5, 10]]
    r_wall = [[17, 5], [18, 6], [19, 7], [20, 8], [21, 9], [22, 10]]
    stable_borders = [[0, 13], [2, 13], [3, 13], [4, 13], [23, 13], [24, 13], [25, 13], [27, 13], [5, 12], [22, 12], [4, 11], [23, 11]]
    wall_locs = l_wall + r_wall + stable_borders
    tiles = filter(lambda _: _, get_tiles(game_state, wall_locs)) # filter out missing walls
    tiles = [tile[0] for tile in tiles] # retrieve singular stationary unit

    # EDIT: we don't need this snippet here; if num_cores > 0, means we finished building our defense, and have some cores to spare.
      # cores_needed += len(wall_locs) - len(tiles)

    weak_tiles = list(filter(lambda tile: tile.stability <= 10, tiles))
    weak_tiles.sort(key=lambda tile: tile.stability)

    tiles_to_fix = weak_tiles[:int(num_cores)]
    coords = [[tile.x, tile.y] for tile in tiles_to_fix]

    if coords:
        game_state.attempt_remove(coords)
    return True


def build_walls(game_state, state):
    """Basic funnel-wall defense."""
    # don't interrupt attack lol:
    if state["emp_mode"] != READY_TO_FIRE:
        left_hole, right_hole = get_holes(state)
        wall_opening_locs = [left_hole, right_hole]
        game_state.attempt_spawn(FILTER, wall_opening_locs)

    # build best wall according to given resources, use scramblers to fill in if needed
    budget = game_state.number_affordable(FILTER)

    # exclude these points:
    holes = set(tuple(lst) for lst in get_holes(state))

    # calculate walls and cost
    cheap_borders = [list(tup) for tup in CHEAP_BORDERS - holes]
    cheap_borders_cost = get_need_to_build(game_state, FILTER, cheap_borders)
    stable_borders = [list(tup) for tup in STABLE_BORDERS - holes]
    stable_borders_cost = get_need_to_build(game_state, FILTER, stable_borders)

    # prefer stable ones if it's same price or cheaper
    if stable_borders_cost <= cheap_borders_cost:
        cheap_borders = stable_borders
        cheap_borders_cost = stable_borders_cost

    l_wall = [list(tup) for tup in L_WALL - holes]
    l_wall_cost = get_need_to_build(game_state, FILTER, l_wall)
    r_wall = [list(tup) for tup in R_WALL - holes]
    r_wall_cost = get_need_to_build(game_state, FILTER, r_wall)

    game_state.attempt_spawn(FILTER, l_wall)
    if budget < l_wall_cost:
        state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[7,6]])

    game_state.attempt_spawn(FILTER, r_wall)
    if budget < l_wall_cost + r_wall_cost:
        state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[20,6]])

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
        path = game_state.find_path_to_edge([3,10], TOP_RIGHT)
        if path is None or len(path) < 8 or not any(game_state.get_attackers(coord, 1) for coord in path[:6]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[3,10]])

    if need_to_build > 0:
        path = game_state.find_path_to_edge([24,10], TOP_LEFT)
        if path is None or len(path) < 8 or not any(game_state.get_attackers(coord, 1) for coord in path[:6]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[24,10]])


def build_inner_defense_1(game_state, state):
    locs = [[12,4], [15,4]]
    num_needed = get_need_to_build(game_state, DESTRUCTOR, locs)
    num_got = game_state.attempt_spawn(DESTRUCTOR, locs)
    if num_got < num_needed and state["scramblers_built"] < 4:
        if game_state.contains_stationary_unit([14,1]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[15,1]])
        elif game_state.contains_stationary_unit([13,1]):
            state["scramblers_built"] += game_state.attempt_spawn(SCRAMBLER, [[12,1]])


def build_outer_defense_1(game_state):
    if game_state.get_resource(game_state.CORES) < 7:
        return
    locs = [[4,12], [23,12]]
    random.shuffle(locs)
    game_state.attempt_spawn(DESTRUCTOR, locs)


def build_inner_defense_2(game_state, state):
    if state["danger_unit"] == FILTER or game_state.get_resource(game_state.CORES > 46):
        locs = [[15,3], [12,3]]
        random.shuffle(locs)
        for loc in locs:
            replace_unit(game_state, loc, FILTER, DESTRUCTOR)
    else:
        pass


def build_outer_defense_2(game_state, state):
    if state["danger_unit"] == FILTER:
        pass
    elif state["danger_unit"] == EMP or game_state.get_resource(game_state.CORES > 46):
        locs = [[3,12], [24,12]]
        random.shuffle(locs)
        for loc in locs:
            replace_unit(game_state, loc, FILTER, DESTRUCTOR)


def build_inner_defense_3(game_state, state):
    if game_state.get_resource(game_state.CORES) > 40:
        game_state.attempt_spawn(DESTRUCTOR, [[11,4], [16,4]])
        #if state["danger_unit"] == FILTER:
        #    pass
        #elif state["danger_unit"] == EMP:
        #    pass


def build_outer_defense_3(game_state, state):
    """unused"""
    if game_state.get_resource(game_state.CORES) > 40:
        if state["danger_unit"] == FILTER:
            pass
        elif state["danger_unit"] == EMP:
            pass



########################### BUILD OFFENSE ######################################
def execute_one_of(fns, *args):
    for fn in fns:
        if fn(*args): #.result
            return True
    return False


def build_offense(game_state, state):
    #execute_one_of([emp_followup_attack_with_scramblers], game_state, state)
    #execute_one_of([emp_followup_attack_with_scramblers, launch_ping_attack, launch_emp_attack], game_state, state)
    execute_one_of([launch_ping_attack, launch_emp_attack], game_state, state)


def emp_followup_attack_with_scramblers(game_state, state):
    """Supposed to be a followup to the emp attack. Against shitty defenses, this will work as well lol."""
    if game_state.get_resource(game_state.CORES, 1) > 24: return False
    #num_new_destructors = int(game_state.get_resource(game_state.CORES, 1) / 6)
    #if num_new_destructors > 5: return False # they can probably recover

    spawn_locs = [[6,7], [21,7]] # TODO: create more launch points if possible
    target_edges = [TOP_RIGHT, TOP_LEFT]

    # calculate paths and damages
    paths = [game_state.find_path_to_edge(spawn_loc, target_edge) for spawn_loc, target_edge in zip(spawn_locs, target_edges)]
    paths = list(filter(lambda path: path and is_edge(path[-1]), paths))
    path_damages = [get_damage_in_path(game_state, path) for path in paths]
    path_infos = list(zip(path_damages, spawn_locs)) # package all the information together

    # find safe paths:
    path_infos = list(filter(lambda p: p[0] == 0, path_infos)) # only get nondestructor paths

    # check if attack is feasible
    num_paths = len(path_infos)
    if num_paths == 0: return False # no paths -> abort
    #if num_new_destructors / num_paths > 0.7: return False # they can probably recover lol

    # number of paths to choose:
    num_scramblers = game_state.number_affordable(SCRAMBLER)
    #group_size = game_state.enemy_health
    #num_groups = int(num_scramblers / group_size)
    #leftovers = num_scramblers % group_size
    #num_groups = min(num_groups, num_paths)
    #if num_groups == 0:
    #    num_groups = 1
    #    leftovers = 0

    ## choose a random set of paths
    #path_infos = random.sample(path_infos, num_groups) # choose as many random paths as possible

    # execute:
    nums = split_evenly(num_scramblers, num_paths)
    for (_, spawn), num in zip(path_infos, nums):
        game_state.attempt_spawn(SCRAMBLER, [spawn], num)

    # add a destructor to counter their scramblers:
    if game_state.get_resource(game_state.CORES) >= 6:
        #game_state.attempt_spawn(FILTER, [14,13])
        game_state.attempt_spawn(DESTRUCTOR, [14,12])
    return True


def launch_ping_attack(game_state, state): # -> bool, True if attack was launched, False otherwise
    if state["emp_mode"] == READY_TO_FIRE or len(state["enemy_units"][DESTRUCTOR]) >= 8:
        return False # do emp attack instead

    #gamelib.debug_write(f"Try to launch ping attack:")
    #if len(state["enemy_units"][DESTRUCTOR]) # TODO: have to identify destructor's "regions" as well...
    # 25% of the time, simply do not attack at all anywhere
    #if random.random() < 0.25: return True # TODO: some work to be done here lol
 
    # calculate paths
    to_right_spawn = [12,1]
    to_left_spawn = [15,1]
    to_right_path = game_state.find_path_to_edge(to_right_spawn, TOP_RIGHT)
    to_left_path = game_state.find_path_to_edge(to_left_spawn, TOP_RIGHT)

    # how many destructor hits do we suffer on each path?
    to_right_hits = get_damage_in_path(game_state, to_right_path)
    to_left_hits = get_damage_in_path(game_state, to_left_path)

    # calculate enemy's most vulnerable path:
    best_spawn = to_right_spawn if to_right_hits < to_left_hits else to_left_spawn
    if random.random() < 0.2: best_spawn = to_right_spawn if to_right_hits >= to_left_hits else to_left_spawn # flip 20% of the time to fuck with enemy, yafeel?
    least_hits = min(to_right_hits, to_left_hits)

    # calculate ROI
    num_pings = game_state.number_affordable(PING)
    predicted_lost_of_pings = min(5, int(game_state.get_resource(game_state.BITS, 1) / 2))
    num_pings -= predicted_lost_of_pings
    surviving_pings = num_pings - int(least_hits / 2) 
    #gamelib.debug_write(f"num_pings={num_pings}, surviving_pings={surviving_pings}, cores={game_state.get_resource(game_state.CORES)}.")
    if (surviving_pings > 5 and (game_state.get_resource(game_state.CORES) > 4) or game_state.game_map[13,0] and game_state.game_map[13,0][0].unit_type == ENCRYPTOR): # solid investment, needs 1 encryptor to get the ping power spike
        game_state.attempt_spawn(ENCRYPTOR, [[13,0]])
        game_state.attempt_spawn(PING, [best_spawn], num=num_pings)
        state["attack_log"][game_state.turn_number] = ["PING", game_state.enemy_health]
        return True
    return False
    # some crazy ping shit
    #game_state.attempt_spawn(ENCRYPTOR, [[13,0], [14,0]]) 
    #if game_state.get_resource(game_state.BITS) > 16 + game_state.turn_number / 8:
    #    game_state.attempt_spawn(PING, random.sample([[12,1], [15,1]], 1), num=50)
    #if game_state.get_resource(game_state.CORES) > 20:
    #    locs = [[10, 4], [17, 4], [10, 3], [17, 3], [11, 2], [12, 2], [15, 2], [16, 2], [12, 1], [15, 1]]
    #    random.shuffle(locs)
    #    game_state.attempt_spawn(ENCRYPTOR, locs)
    #if game_state.get_resource(game_state.BITS) > 16 + game_state.turn_number / 8:
    #    game_state.attempt_spawn(PING, random.sample([[13,0], [14,0]], 1), num=50)


def reserve_resources_for_emp(game_state, state):
    if state["emp_mode"] == READY_TO_FIRE:
        # "reserve hack" for 1 CORE needed to act as piston:
        game_state._GameState__set_resource(game_state.BITS, -2)


def launch_emp_attack(game_state, state):
    # prioritize pings or scramblers
    num_enemies = len(state["enemy_units"][DESTRUCTOR]) 
    if game_state.get_resource(game_state.BITS) > 5 * num_enemies:
        return False
    # useful in both rounds:
    required_emps = 3
    if num_enemies >= 3: required_emps = 4
    if num_enemies >= 7: required_emps = 5
    if num_enemies >= 13: required_emps = 6
    if game_state.game_map[2,15] and game_state.game_map[2,15].unit_type == DESTRUCTOR:
        required_emps += 1

    #if num_enemies >= 17: required_emps = 7
    #gamelib.debug_write(f"num_enemies = {num_enemies}")

    # LOAD UP THE EMP CANNON:
    if state["emp_mode"] == UNLOADED:
        num_bits_next_turn = game_state.project_future_bits(1, 0)
        if num_bits_next_turn < 3 * required_emps:
            return False

        # predicted to have sufficient bits:
        left_hole, right_hole = get_holes(state)
        game_state.attempt_remove([left_hole, right_hole]) # remove both holes
        state["emp_mode"] = READY_TO_FIRE
        return True

    # FIRE THE CANNON
    elif state["emp_mode"] == READY_TO_FIRE:
        # undo "reserve hack" for CORES:
        game_state._GameState__set_resource(game_state.BITS, 2)

        left_hole, right_hole = get_holes(state)
        left_spawn, right_spawn = [9,4], [18,4]
        left_piston, right_piston = [10,4], [17,4]

        # left pathing test:
        game_state_cp = copy.deepcopy(game_state)
        game_state_cp.attempt_spawn(FILTER, [left_piston])
        left_path = game_state_cp.find_path_to_edge(left_spawn, TOP_RIGHT)

        # undo the left pathing test:
        game_state_cp.game_map.remove_unit(left_piston)
        game_state._GameState__set_resource(game_state.BITS, 1)
        # right pathing test:
        game_state_cp.attempt_spawn(FILTER, [right_piston])
        right_path = game_state_cp.find_path_to_edge(right_spawn, TOP_LEFT)

        # TODO: calculate total amount of obstacles, and predict failure. give some room for error if the enemy responds with extra defenses. if failure, then abort. 
        
        viable_paths = []
        if left_hole in left_path: viable_paths.append((left_spawn, left_piston, left_path, right_hole))
        if right_hole in right_path: viable_paths.append((right_spawn, right_piston, right_path, left_hole))
        
        if len(viable_paths) == 0:
            game_state.attempt_spawn(FILTER, [left_piston, right_piston])
            state["emp_mode"] = UNLOADED
            return False

        spawn, piston, path, unused_hole = random.sample(viable_paths, 1)[0]
        
        game_state.attempt_spawn(FILTER, [piston])
        game_state.attempt_spawn(EMP, [spawn], required_emps + 1) # always try to add 1 for safety

        # early clean up just for safety ;) 
        game_state.attempt_spawn(FILTER, [unused_hole])
        game_state.attempt_remove([piston])

        state["emp_mode"] = UNLOADED
        state["emp_round"] += 1
        return True


######################## SCRAMBLER DEFENSE #####################################
def launch_scrambler_defense(game_state, state):
    # defend against ping rush with scramblers:
    potential_enemy_pings = game_state.get_resource(game_state.BITS, 1)
    hp_per_ping = len(state["enemy_units"][ENCRYPTOR]) * 3 + 15
    destructor_hits_per_ping = math.ceil(hp_per_ping / 16)
    #TODO only count destructors in the center:
    destructor_kill_count = int(len(state["player_units"][DESTRUCTOR]) * 6 / destructor_hits_per_ping)
    surviving_pings = potential_enemy_pings - destructor_kill_count
    scramblers_needed = 0
    if surviving_pings > 2:
        scrambler_hits_per_ping = math.ceil(hp_per_ping / 20)
        scrambler_fire_rate = 7
        # purposely round down:
        scramblers_needed = int(scrambler_hits_per_ping * surviving_pings / scrambler_fire_rate)
    # anti emp measures:
    if game_state.get_resource(game_state.BITS, 1) >= 15:
        scramblers_needed = 2
    # more risk:
    scramblers_needed -= 1

    # don't spoil a attack for scrambling:
    my_bits = game_state.get_resource(game_state.BITS)
    if state["emp_mode"] == READY_TO_FIRE and game_state.project_future_bits(1, 0, my_bits - scramblers_needed) < 12:
        # TODO dunno what best strat is here, to focus on defense or offense?
        #scramblers_needed = 0
        if random.random() < 0.7: scramblers_needed = 0 # focus on attack 70% of time
    # unless we about to get rickity rekt:
    if scramblers_needed > 0:
        #gamelib.debug_write(f"Generating {scramblers_needed} scramblers.")
        if units_at(game_state, [[13,1], [14,2]]):
            scrambler_locs = [[9,4]]
        elif units_at(game_state, [[13,2], [14,1]]):
            scrambler_locs = [[18,4]]
        else:
            scrambler_locs = [[9,4], [18,4]]
        for i in range(scramblers_needed):
            game_state.attempt_spawn(SCRAMBLER, [scrambler_locs[i % len(scrambler_locs)]])


def send_scramblers(game_state, state):
    pass

