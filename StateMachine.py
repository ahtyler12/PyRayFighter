from State import State
from typing import List
from State import State, Idle,Move
from InputComponent import InputComponent

class StateMachine:
    def __init__(self,_inputs: InputComponent):
        self.states: List[State] = [Idle(_inputs), Move(_inputs)]
        self.starting_state = self.states[0]
        if self.starting_state is not None:
            self.starting_state.enter()
        else:
            print("No starting state was passed")
            self.starting_state = self.states[0]
        self.current_state = self.starting_state
    def update(self):
        new_state = self.get_state_by_id(self.current_state.update())
        if new_state is not None:
            self.change_state(new_state)
    
    def change_state(self, next_state: State):
        if self.current_state:
            self.current_state.exit()
        if next_state is not None:
            self.current_state = next_state
        self.current_state.enter()
    def get_state_by_id(self, state_id:int) -> State:
        for state in self.states:
            if state.state_id == state_id:
                return state
        
