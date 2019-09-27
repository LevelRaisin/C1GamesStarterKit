import gamelib
import random
import math
import warnings
from sys import maxsize
import json

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)

    def on_game_start(self, config):
        self.config = config

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        # waste our resources
        locs = [[12, 1], [13, 1], [14, 1], [15, 1], [13, 0], [14, 0]]
        game_state.attempt_remove(locs)
        game_state.attempt_spawn("DF", locs)

        game_state.submit_turn()

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
