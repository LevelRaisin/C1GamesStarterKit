from constants import *
import math

def build_encryptors(game_state, state, config, curr_cores):
    # use all cores to build encryptors
    encryptor_cost = config["unitInformation"][1]["cost"]
    start_cores = config["resources"]["startingCores"]
    if game_state.turn_number == 0:
        num_encryptors = math.floor(start_cores / encryptor_cost)
    else:
        num_encryptors = math.floor((start_cores + curr_cores)
                                        / encryptor_cost)
    # form a 2 x k rectangles
    height = int(math.floor(num_encryptors / 2))
    encryptor_locations = [[x, y] for x in (13, 14) for y in range(2, max(14, 2+height))]
    game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)
