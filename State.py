from enum import Enum
import InputComponent
from HitEvent import HitEvent
import Hitbox
from Entity import Entity
import MovementComponent
from typing import List
from pyray import *

class STATUS(Enum):
    STANDING = 0
    AIRBOURNE = 1
    GROUNDED = 2

class ATTACK_STATE(Enum):
    STARTUP = 0
    ACTIVE = 1
    RECOVERY = 2

class COUNTERHIT(Enum):
    NONE = 0
    COUNTER = 1
    HARDCOUNTER =2

class INVULTYPE(Enum):
    NONE = 0
    STRIKE = 1
    THROW = 2
    FULL = 3

class MoveFlag(Enum):
    MOVE_RIGHT = 0
    MOVE_LEFT = 1


class State:
    state_frame: int = 0
    state_id: int = 0
    animation_index: int = 0
    status = STATUS.STANDING
    counter = COUNTERHIT.NONE
    invul = INVULTYPE.NONE
    parent: Entity = None
    hit_events: list[HitEvent]
    #_parent: Entity
    def __init__(self, _input_component: InputComponent, _movement_component: MovementComponent):
        self.input_component = _input_component
        self.movement_component = _movement_component
        self.hurt_boxes: List[BoundingBox] = [] #Hurt boxes are stored as a List of Rectangles with an offset as the position. That way they are always at the entities location
        self.push_box: BoundingBox = BoundingBox(Vector3(50,100,1), Vector3(50,100,1))
        # self.parent = _parent if _parent is not None else None
    
    def update(self):
        #process input
        self.state_frame += 1
        pass

    def enter(self):
        self.state_frame = 0
        #start playing animation somewhere here

    def exit(self):
        pass
    
    def is_on_ground(self) -> bool:
        return False
    
    def reset_hit_settings(self):
        pass

    def get_hitbox_data(self) -> list[HitEvent]:
        temp_event: HitEvent = HitEvent()
        
        #Need to pass in some form of the owning entities attack data

        return self.hit_events

    def create_hitboxes(self):
        for event in self.hit_events:
            if self.state_frame > event.active_frame and self.state_frame < event.frame_duration:
                new_box: Hitbox = Hitbox(Rectangle(event.x_offset, event.y_offset, event.x_size, event.y_size), event) #Make a way to change offset depending on if the parent is facing left or right
    
    def face_opponent(self):
        pass

class Idle(State):
    def __init__(self, _input_component: InputComponent, _movement_component: MovementComponent):
        self.state_id = 1
        super().__init__(_input_component,_movement_component)
        
        self.hurt_boxes.insert(0,BoundingBox(Vector3(30, 0, 0),Vector3(40,40,40)))

    def update(self):
        # if self.input_component.current_input & InputComponent.InputCommand.Right:
        #     print("Pressed Right")
        #     return 2
        # elif self.input_component.is_input_held(InputComponent.InputCommand.Left,self.movement_component.facing_right):
        #     print("Pressed Leftt")
        #     return 2
        return None
    
    def enter(self):
        print("Entering Idle State")
        self.movement_component.velocity.x = 0
    
    def exit(self):
        print("Exiting Idle State")

class Move(State):
    def __init__(self, _input_component: InputComponent, _movement_component: MovementComponent):
        self.state_id = 2
        super().__init__(_input_component,_movement_component)
        
        self.hurt_boxes.insert(0,BoundingBox(Vector3(30, 0, 0),Vector3(40,40,40)))

    def update(self):
        pass
        # if  not self.input_component.is_input_held(InputComponent.InputCommand.Right, self.movement_component.facing_right) or not self.input_component.is_input_held(InputComponent.InputCommand.Left,self.movement_component.facing_right):
        #     return 1

    
    def enter(self):
        print("Entering Move State")
        # if self.input_component.current_input & InputComponent.InputCommand.Right:
        #      self.movement_component.velocity.x = 10 
        # elif self.input_component.current_input & InputComponent.InputCommand.Left:
        #      self.movement_component.velocity.x = -10 
       
    
    def exit(self):
        print("Exiting Move State")
        self.push_box = BoundingBox(Vector3(50,100,1), Vector3(50,100,1))