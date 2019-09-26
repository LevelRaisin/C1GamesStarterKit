
def build_stage(self, game_state, stage):
    current_stage = stage.build()
    if current_stage == SUCCESSFUL_STAGE_BUILD:
        return build_stage(self, game_state, stage.next_stage)
    else:
        return current_stage


class State:
    def __init__(self, my_stage):
        self.my_stage = my_stage
        self.next_stage = None


    def build(self, game_state):




def _build_initial_state(self, game_state):
    destructor_locations = [[11,9], [16,9]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

    filter_locations = []
    filter_locations += [[0,13], [1,13], [2,13], [25,13], [26,13], [27,13]]
    filter_locations += [[3,12], [4,11], [23,11], [24,12]]
    filter_locations += [[i, 10] for i in range(5, 12)]
    filter_locations += [[i, 10] for i in range(16, 23)]
    filter_locations += [[12,9], [15,9]]
    game_state.attempt_spawn(FILTER, filter_locations)

STATE_INITIAL = State(_build_initial_state)

    
def _build_secondary_central_destructors(self, game_state):
    destructor_locations = [[12,8], [15,8]]
    game_state.attempt_spawn(DESTRUCTOR, destructor_locations)
STATE_SECURE_CENTRAL = State(_build_secondary_central_destructors)
