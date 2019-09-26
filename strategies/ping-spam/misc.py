from collections import defaultdict
import gamelib


def remove_specific_unit_type(unit_type, locations, game_state):
    game_map = game_state.game_map
    for location in locations:
        if game_map[location].unit_type == unit_type:
            game_state.attempt_remove(location)


def build_complete(unit_type, locations, game_state):
    if type(unit_types) != type([]):
        unit_types = [unit_types]

    for location in locations:
        found_unit_type = False
        for unit_type in unit_types:
            if game_state.game_map[location].unit_type == unit_type:
                found_unit_type = True
                break
        if not found_unit_type:
            return False
    return True
        

def split_resources_with_preference(num_needed, resources_available, preference, alternative):
    assert(alternative.cost < preference.cost)

    # solve the following problem:
    # max
    #   num_alternative
    # s.t.
    #   num_preference * preference.cost + num_alternative * alternative.cost < resource_available
    #   num_preference + num_alternative == num_needed

    # first use cheap 
    num_preference = 0
    num_alternative = num_needed
    resources_left = resources_available - num_needed * alternative.cost
    while resources_left + alternative.cost - preference.cost >= 0 and num_preference < num_needed:
        num_preference += 1
        num_alternative -= 1
        resources_left += alternative.cost - preference.cost

    return num_preference, num_alternative


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

def locate_units(game_state, is_player):
    # TODO: modify so that we differentiate between units on the edges, in the center, or by the border center
    all_units = defaultdict(list) 
    all_locations = PLAYER_LOCATIONS if is_player else ENEMY_LOCATIONS
    for location in all_locations:
        units = game_state.game_map[location]
        for unit in units:
            all_units[unit.unit_type].append(unit)
    return all_units


def units_at(game_state, locations):
    for location in locations:
        if not game_state.contains_stationary_unit(location):
            return False
    return True


def empty_at(game_state, locations):
    for location in locations:
        if game_state.contains_stationary_unit(location):
            return False
    return True


def calculate_build_plan_cost(game_state, build_plan):
    cost = 0
    m = game_state.game_map
    for unit_type, locs in build_plan.items():
        for loc in locs:
            if m[loc].unit_type != unit_type:
                cost += unit_type.cost
    return cost



