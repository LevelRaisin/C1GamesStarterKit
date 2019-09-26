import gamelib
import random
import math
import warnings
from sys import maxsize
import json
from misc import (
    remove_specific_unit_type,
    build_complete,
    split_resources_with_preference,
)

SUCCESS_DAG_STATE = -1
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
        self.build_initial_defense(game_state)


    def execute_dag(self, game_state, dag):
        for index, taskname in enumerate(dag):
            task = getattr(self, taskname)
            success = task(game_state)
            if not success:
                return index
        return SUCCESS_DAG_STATE


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.
        

        ####### Can specify which type of gameplay we want to use here: ########
        # TODO other gameplays:

        # if self.gameplay_type == ...
        self.gameplay_normal(game_state)

    
    def gameplay_normal(self, game_state):
        # initial turns:
        if game_state.turn_number <= 1:
            self.execute_initial_strategy(game_state, game_state.turn_number)
            game_state.submit_turn()
            return

        # emergency response:
        # TODO

        # build static defense here:
        self.build_walls(game_state)
        self.build_central_defense_1(game_state)
        self.build_outer_defense_1(game_state)
        
        # launch scrambler defense:
        launch_scrambler_defense(self, game_state)

        # launch attack:
        # TODO tweak these parameters:
        self.launch_emp_attack(game_state, num_emps=4, bit_leniency=2)

        # extra static defense:
        # TODO: do we even want this? or just save cores for recovery
        self.build_central_defense_2(game_state)
        self.build_outer_defense_2(game_state)

        game_state.submit_turn()


    ########################## INITIAL STRATEGY ################################
    def execute_initial_strategy(self, game_state, turn_number):
        if turn_number == 0:
            return

        if turn_number == 1:
            loc = [12,3] if random.random() > 0.5 else [15,3]
            game_state.attempt_spawn(DESTRUCTOR, [loc])
            self.launch_scrabler_defense(game_state)


    ############################ SCRAMBLER DEFENSE AGAINST PING RUSH ###########
    def launch_scrambler_defense(self, game_state):
        # defend against ping rush with scramblers:
        enemy_encryptors = locate_enemy_units(game_state, ENCRYPTOR)
        potential_enemy_pings = game_state.get_resource(game_state.BITS, 1)
        hp_per_ping = enemy_encryptors * 3 + 15
        destructor_hits_per_ping = math.ceil(hp_per_ping / 16)
        destructor_kill_count = int(self.num_destructors * 6 / destructor_hits_per_ping)
        surviving_pings = potential_enemy_pings - destructor_kill_count
        if surviving_pings > 2:
            scrambler_hits_per_ping = math.ceil(hp_per_ping / 20)
            scrambler_fire_rate = 7
            # purposely round down:
            scramblers_needed = int(scramber_hits_per_ping * surviving_pings / scrambler_fire_rate)
            if scramblers_needed > 0:
                if units_at(game_state, [[13,1], [14,2]]):
                    scrambler_locs = [[12,1]]
                elif units_at(game_state, [[13,2], [14,1]]):
                    scrambler_locs = [[15,1]]
                else:
                    scrambler_locs = [[12,1], [15,1]]
                for i in range(scramblers_needed):
                    game_state.attempt_spawn(SCRAMBLER, [scrambler_locs[i % len(scrambler_locs)]])


    ######################## EMP ATTACK #######################################
    def launch_emp_attack(self, game_state, num_emps=4, bit_leniency=2):
        if self.mode == DEFENSE_MODE:
            # must spawn no matter what, to prevent immediate attack:
            game_state.attempt_spawn(FILTER, [[1,13], [26,13]])

            # TODO: predict enemy EMP attack, counter with stacking of bits

            # if have enough for attack, open walls to prepare for attack
            if project_future_bits(1, 0) >= 3 * num_emps + bit_leniency: 
                game_state.attempt_remove([[1,13], [26,13]])

            # set ready flag for attack:
            self.mode = ATTACK_MODE
            return

        if self.mode == ATTACK_MODE:
            # choose direction, and calculate coordinates for that direction
            is_left = random.random() < 0.5
            guidance_walls = [[12,3], [13,2], [14,1]] if is_left else [[15,3], [14,2], [13,1]]
            wall_opening = [1,13] if is_left else [26,13]
            other_wall_opening = [26,13] if is_left else [1,13]
            emp_placement = [13,0] if is_left else [14,0]

            # last minute check for all resources
            if (game_state.get_resource(game_state.BITS) >= 3 * num_emps and # bits needed for emp
                game_state.get_resource(game_state.CORES) >= 2 and # cores needed for walling
                empty_at(game_state, wall_opening)): # opening in wall
                game_state.attempt_spawn(FILTER, guidance_walls) # build guidance walls
                game_state.attempt_spawn(FILTER, [other_wall_opening]) # fill in opposite opening
                # last last minute check:
                pathing = game_state.navigation.navigate_multiple_endpoints(emp_placement, [wall_opening], game_state)[0]
                if abs(len(pathing) - 23) > 4:
                    # abort:
                    game_state.attempt_spawn(FILTER, [wall_opening, other_wall_opening])
                else:
                    # commence attack!
                    game_state.attempt_spawn(EMP, [emp_placement], num=num_emps) # place emps
            else:
                # otherwise, cancel by filling in all the openings to prevent attack:
                game_state.attempt_spawn(FILTER, [wall_opening, other_wall_opening])
            # recover in defense mode:
            self.mode = DEFENSE_MODE


    ########################### EMERGENCY RESPONSE #############################

    def wall_emergency(self, game_state):
        # TODO
        pass


    def central_emergency(self, game_state):
        # TODO
        pass


    def outer_emergency(self, game_state):
        # TODO
        pass


    ######################### STATIC DEFENSE ###################################

    # central_defense_1 + shortcutted walls (because of 40 core constraint)
    def build_initial_defense(self, game_state):
        filter_locations =  [[0,13], [2,13], [25,13], [27,13]]
        filter_locations += [[3+i,12-i] for i in range(8)]
        filter_locations += [[17+i,5+i] for i in range(8)]
        filter_locations += [[11,5], [12,5],  [15,5], [16,5]]
        game_state.attempt_spawn(FILTER, filter_locations)

        destructor_locations = [[12,4], [15,4]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

        
    def build_walls(self, game_state):
        # don't interrupt attack lol:
        if self.mode != ATTACK_MODE:
            wall_opening_locs = [[1,13], [26,13]]
            game_state.attempt_spawn(FILTER, filter_locations)

        # build best wall according to given resources, use scramblers to fill in if needed
        # TODO


    def build_central_defense_1(self, game_state):
        destructor_locations = [[12,4], [15,4]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)


    def build_central_defense_2(self, game_state):
        # TODO
        pass


    def build_outer_defense_1(self, game_state):
        # TODO
        pass


    def build_outer_defense_2(self, game_state):
        # TODO
        pass

    
if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
