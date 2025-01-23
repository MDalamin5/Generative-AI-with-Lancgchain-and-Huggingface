from transitions import Machine

class TutorBot(object):
    states = ['INTRO', 'STEP_IN_PROGRESS', 'CHECK_UNDERSTANDING', 'DONE']

    def __init__(self):
        self.machine = Machine(model=self, states=TutorBot.states, initial='INTRO')
        self.machine.add_transition(trigger='start_step', source='INTRO', dest='STEP_IN_PROGRESS')
        self.machine.add_transition(trigger='check_understanding', source='STEP_IN_PROGRESS', dest='CHECK_UNDERSTANDING')
        self.machine.add_transition(trigger='finish', source='CHECK_UNDERSTANDING', dest='DONE')
