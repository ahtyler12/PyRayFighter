from State import *
from Entity import Entity
from pyray import *
import InputComponent


class Idle(State):
    def __init__(self, _parent, _input_component):
        super().__init__(_parent, _input_component)
        self.status = STATUS.STANDING
        if self.parent.position.y < 300:
            self.parent.position.y = 300
    def enter(self):
        self.state_frame = 0
        #start playing animation somewhere here        
    def update(self):
        self.face_opponent()
        #process inputs here
    def exit(self):
        pass

class Crouch(State):
    def __init__(self, _parent, _input_component):
        super().__init__(_parent, _input_component)
    
    def update(self):
        self.face_opponent()
        #process inputs here

class Jump(State):
    def __init__(self, _parent, _input_component):
        super().__init__(_parent, _input_component)
    
    def update(self):
        self.face_opponent()
        #process inputs here

class Move(State):
    def __init__(self, _parent, _input_component):
        super().__init__(_parent, _input_component)
    
    def update(self):
        self.face_opponent()
        #process inputs here