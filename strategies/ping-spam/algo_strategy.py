import gamelib
import random
import math
import warnings
from sys import maxsize
import json
from misc import *

DEFENSE_MODE = 0
ATTACK_MODE = 1
"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]

        # This is a good place to do initial setup
        self.mode = DEFENSE_MODE
        self.state = {
            "attack_log": {
                "PING": [0,0],
                "EMP": [0,0],
                "SCRAMBLER": [0,0],
            },
            "emp_mode": UNLOADED,
            "danger_unit": PING,
            "navigator": gamelib.navigation.ShortestPathFinder(),
        }

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('>> ping-spam: Turn {}'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings. 

        curr_cores = game_state.get_resource(game_state.CORES)
        curr_bits = game_state.get_resource(game_state.BITS)

        # Spam encrytors + ping combo
        build_encryptors(game_state, self.state, self.config, curr_cores)
        game_state.attempt_spawn(PING, [13,0], num=35)

        game_state.submit_turn()

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
