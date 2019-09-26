from functools import partial

#class Dag:
#    SUCCESS = -1
#    def __init__(self):
#        self.game_state = None
#        self.tasks = []
#        self.current_task = 0
#    
#    def run(self):
#        for task in self.tasks[self.current_task:]:
#            result = task.run()
#            if not result: return self.current_task
#            self.current_task += 1
#        return Dag.SUCCESS
#
#    def reset(self, game_state, starter_task = 0):
#        self.current_task = starter_task 


class Task:
    def __init__(self, game_state, fn, args=[], kwargs={}, checker=lambda: True, checker_args=[], checker_kwargs={}, children=[]):
        self.game_state = game_state
        self.task = partial(fn, game_state, *args, **kwargs)
        self.checker = partial(checker, game_state, *checker_args, **checker_kwargs)
        self.children = children 

    def run(self):
        self.task()
        if not self.checker(): return False
        for child in self.children:
            if not child.run(): return False
        return True
