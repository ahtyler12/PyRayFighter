from enum import Enum,Flag, auto
from typing import List
from pyray import *

class InputCommand(Flag):
    NONE = auto()
    Up = auto()
    Down = auto()
    Left = auto()
    Right = auto()
    Light = auto()
    Medium = auto()
    Heavy = auto()


class MotionNames(Enum):
    FIRST =0
    QCF =1
    QCB=2
    DP=3
    RDP=4
    HCF=5
    HCB=6
    LAST=7


class InputComponent:
    def __init__(self):
        self.is_keyboard: bool = False
        self.MotionInputs: dict = {
            MotionNames.FIRST:[0,0,0],
            MotionNames.QCF:[2,3,6],
            MotionNames.QCB:[2,1,4],
            MotionNames.DP:[6,2,3],
            MotionNames.RDP:[4,2,1],
            MotionNames.HCF:[4,1,2,3,6],
            MotionNames.HCB:[6,3,2,1,4]
            }
        self.buffer_size: int = 60
        self.buffer_index: int = self.buffer_size -1
        self.input_buffer: List[InputCommand] = [InputCommand.Up for input in range(self.buffer_size)]
        self.current_input = InputCommand.NONE
    
    def get_local_input(self,gamepad_index: int = 0, is_keyboard: bool = False ) -> InputCommand:
        if not is_keyboard:
            if is_gamepad_available(gamepad_index):
                if is_gamepad_button_down(gamepad_index, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_UP):
                    return InputCommand.Up
                elif is_gamepad_button_down(gamepad_index, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_DOWN):
                    return InputCommand.Down
                if is_gamepad_button_down(gamepad_index, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT):
                    return InputCommand.Right
                elif is_gamepad_button_down(gamepad_index, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT):
                    return InputCommand.Left
                
                return InputCommand.NONE
        else:
            if is_key_pressed(KeyboardKey.KEY_UP):
                return InputCommand.Up
            elif is_key_pressed(KeyboardKey.KEY_DOWN):
                return InputCommand.Down
            if is_key_pressed(KeyboardKey.KEY_LEFT):
                return InputCommand.Left
            elif is_key_pressed(KeyboardKey.KEY_RIGHT):
                return InputCommand.Right
            return InputCommand.NONE
    
    def update_input_buffer(self) -> InputCommand:
        self.buffer_index = (self.buffer_index + 1) % len(self.input_buffer)
        self.input_buffer[self.buffer_index] = self.current_input
    
    def get_current_command(self) -> InputCommand:
        return self.input_buffer[self.buffer_index]
    
    def get_last_input_command(self):
        return self.input_buffer[(len(self.input_buffer)- 1 + self.buffer_size) % self.buffer_size]
    
    def is_input_held(self, _input: InputCommand, facing_right:bool)-> bool:
        last_input = self.get_last_input_command()
        pressed: bool = False
        if last_input & InputCommand.Up:
            pressed = True
        elif last_input & InputCommand.Down:
            pressed = True
        elif last_input & InputCommand.Right:
            pressed = True
        elif last_input & InputCommand.Left:
            pressed = True

        return pressed
    
    def was_pressed_on_frame(self, _input: InputCommand, frame: int, facing_right: bool) -> bool:
        current_input: InputCommand = self.get_current_command()
        last_input: InputCommand = self.get_last_input_command()

        left_check: bool = (current_input & InputCommand.Left) and not (last_input & InputCommand.Left)
        right_check: bool = (current_input & InputCommand.Right) and not (last_input & InputCommand.Right)

        pressed: bool = False

        match _input:
            case InputCommand.Up:
                return (current_input & InputCommand.Up) and not (last_input & InputCommand.Up)
            case InputCommand.Down:
                return (current_input & InputCommand.Down) and not (last_input & InputCommand.Down)
            case InputCommand.Right:
                return (current_input & InputCommand.Right) and not (last_input & InputCommand.Right)
            case InputCommand.Left:
                return (current_input & InputCommand.Left) and not (last_input & InputCommand.Left)
        
        return False
    
    
    def was_input_buffered(self, _input: InputCommand, duration: int, facing_right: bool):
        i = 0
        while i < duration:
            if self.was_pressed_on_frame(_input,(self.buffer_size - 1 + self.buffer_index)- i, facing_right):
                return True
            i+=1
        return False
    def was_input_pressed(self, _input: InputCommand, facing_right: bool):
        current_input: InputCommand = self.get_current_command()
        last_input: InputCommand = self.get_last_input_command()

        left_check: bool = (current_input & InputCommand.Left) and not (last_input & InputCommand.Left)
        right_check: bool = (current_input & InputCommand.Right) and not (last_input & InputCommand.Right)

        pressed: bool = False

        match _input:
            case InputCommand.Up:
                pressed = (current_input & InputCommand.Up) and not (last_input & InputCommand.Up)
            case InputCommand.Down:
                pressed = (current_input & InputCommand.Down) and not (last_input & InputCommand.Down)
            case InputCommand.Right:
                return (current_input & InputCommand.Right) and not (last_input & InputCommand.Right)
            case InputCommand.Left:
                pressed = (current_input & InputCommand.Left) and not (last_input & InputCommand.Left)
        
        return pressed 

    def check_numpad_direction(self, _input: InputCommand, numpad_direction: int, facing_right: bool)-> bool:
        if facing_right:
            forward = InputCommand.Right
            back = InputCommand.Left
        else:
            forward = InputCommand.Left
            back = InputCommand.Right
        
        match numpad_direction:
            case 1:
                #print("Down Back gave a response of: ", (_input & InputCommand.Down & back))
                return _input & InputCommand.Down and (_input & back)
            case 2:
                #print("Down gave a response of: ", _input & InputCommand.Down and not ((_input & back) or (_input & forward)))
                return _input & InputCommand.Down and not ((_input & back) or (_input & forward))
            case 3:
                return _input & InputCommand.Down and (_input & forward)
            case 4:
                print("Back gave a response of: ", _input & back and not ((_input & InputCommand.Up) or (_input & InputCommand.Down)))
                return _input & back and not ((_input & InputCommand.Up) or (_input & InputCommand.Down))
            case 6:
                return _input & forward and not ((_input & InputCommand.Up) or (_input & InputCommand.Down))
            case 7:
                return _input & InputCommand.Up and (_input & back) 
            case 8:
                return _input & InputCommand.Up and not ((_input & back) or (_input & forward))
            case 9:
                return _input & InputCommand.Up and  (_input & forward)
            case _:
                print("Neutral input detected")
                return False
            

    def was_motion_executed(self, motion_name: MotionNames, time_limit: int, facing_right: bool):
        adjusted_timelimit = time_limit

        if adjusted_timelimit > self.buffer_size + self.buffer_index:
            adjusted_timelimit = self.buffer_size + self.buffer_index
        
        current_motion_index: int = 0

        motion_list = self.MotionInputs[motion_name]

        for count in range(adjusted_timelimit):
            buffer_position: int = (self.buffer_size - (adjusted_timelimit - 1) + self.buffer_index + count) % self.buffer_size
            command: InputCommand = self.input_buffer[buffer_position]

            if self.check_numpad_direction(command, motion_list[current_motion_index], facing_right):
                current_motion_index += 1
                if current_motion_index > len(motion_list):
                    return True
        
        return False
