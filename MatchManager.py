from pyray import *
from InputComponent import InputCommand, MotionNames
from StateMachine import StateMachine, State
from components import ReactionComponent, InputComponent, MovementComponent
from State import STATUS
from HitEvent import HitEvent
from Entity import Entity
import os
import sys
import logging
import pickle
from typing import List
from enum import Enum,Flag, auto
import enet
import math

PACKET_HISTORY_SIZE = 10

class NetSyncType(Enum):
    DELAY = 0
    ROLLBACK = 1

class NetworkType(Enum):
    UNSET = 0
    HOST = 1
    CLIENT = 2

class MatchState(Enum):
    PREMATCH = 0
    CHARACTER_INTRO_A = 1
    CHARACTER_INTRO_B = 2
    MATCH_BEGIN = 3
    MATCH_ACTIVE = 4
    ROUND_OVER = 5
    MATCH_OVER = 6
    CHARACTER_DEFEAT= 7
    CHARACTER_VICTORY = 8
    MATCH_RESULTS = 9


class GameState:
    def __init__(self):
        self.entities = [Entity(), Entity()] 
        self.movement = [MovementComponent(), MovementComponent()]
        self.inputs = [InputCommand.NONE, InputCommand.NONE]
        self.frame_count: int = 0

class NetInputPackage:
    def __init__(self):
        self.Frame = 0
        self.Input_History = [InputCommand.NONE for i in  range(PACKET_HISTORY_SIZE)]

class MatchManager:
    def __init__(self):
        #TODO: Add in a method of passing in the class of the entities to spawn from the character select menu as well as their input methods
        self.input_components = [InputComponent(), InputComponent()]
        self.INPUT_HISTORY_SIZE = 3*60*60 # Enough inputs for 3 60 second rounds at 60fps
        self.input_history = [[InputCommand.NONE, InputCommand.NONE] for i in range(2)]
        self.inputs = [InputCommand.NONE, InputCommand.NONE]
        self.movement_components:List[MovementComponent] =  [MovementComponent(), MovementComponent()]
        self.state_machines: List[StateMachine] = [StateMachine(self.input_components[0], self.movement_components[0]), StateMachine(self.input_components[0], self.movement_components[0])]
        self.reaction_components:List[ReactionComponent] = [ReactionComponent(), ReactionComponent()]
        self.hit_events: List[HitEvent] = []
        self.last_hit_event: HitEvent = None
        self.entities = [Entity(), Entity()]
        self.movement_components[0].position = Vector3(-100,0,0)
        self.entities[0].facing_right = True
        self.movement_components[1].position = Vector3(100,0,0)
        self.entities[1].facing_right = False
        self.entities[1].is_player_1 = False
        self.camera = Camera3D()
        self.camera.fovy = 60.0
        self.camera.up = Vector3(0,1.0,0)
        self.camera.position = Vector3(0,50,350)
        self.camera.target = Vector3(0.0,50.0,0.0)
        self.game_state = GameState()
        self.saved_state = GameState()
        self.match_state = MatchState.MATCH_ACTIVE
        self.health_bar_width = 250
        self.save_state()
    
    def update(self):
        if is_key_pressed(KeyboardKey.KEY_F1):
            self.load_state()
        self.camera.target = Vector3(0,50,0)
        match self.match_state:
            case MatchState.PREMATCH:
                pass
            case MatchState.CHARACTER_INTRO_A:
                pass
            case MatchState.CHARACTER_INTRO_B:
                pass
            case MatchState.MATCH_BEGIN:
                pass
            case MatchState.MATCH_ACTIVE:
                for input in self.input_components:
                    input.current_input = input.get_local_input(0)
                    input.update_input_buffer()
                self.update_physics()
                self.update_collisions()
                self.update_reactions()
                self.update_hit_events()
            case MatchState.ROUND_OVER:
                pass
            case MatchState.MATCH_OVER:
                pass
            case MatchState.CHARACTER_DEFEAT:
                pass
            case MatchState.CHARACTER_VICTORY:
                pass
            case MatchState.MATCH_RESULTS:
                pass
        self.game_state.frame_count += 1

        for sm in self.state_machines:
            sm.update()

    def draw(self):
        draw_text(str(self.game_state.frame_count), int(get_screen_width()/2),50,24,BLACK)
        draw_text("Current x velocity: "+str(self.movement_components[0].velocity.x), 10, 30, 12, RED)     
        draw_text("Current x velocity: "+str(self.movement_components[0].velocity.x), int(get_screen_width() - 10), 30, 12, BLUE)     
        match self.match_state:
            case MatchState.PREMATCH:
                pass
            case MatchState.CHARACTER_INTRO_A:
                pass
            case MatchState.CHARACTER_INTRO_B:
                pass
            case MatchState.MATCH_BEGIN:
                pass
            case MatchState.MATCH_ACTIVE:
                self.show_match_hud()
            case MatchState.ROUND_OVER:
                pass
            case MatchState.MATCH_OVER:
                pass
            case MatchState.CHARACTER_DEFEAT:
                pass
            case MatchState.CHARACTER_VICTORY:
                pass
            case MatchState.MATCH_RESULTS:
                pass
        begin_mode_3d(self.camera)
        for index in  range(len(self.entities)):
            draw_bounding_box(BoundingBox(Vector3(self.entities[index].position.x - self.state_machines[index].current_state.push_box.min.x, self.entities[index].position.y - self.state_machines[index].current_state.push_box.min.y,1),
                                          Vector3(self.entities[index].position.x + self.state_machines[index].current_state.push_box.max.x,self.entities[index].position.y + self.state_machines[index].current_state.push_box.max.y,1)),
                                          YELLOW)            
        for entity in self.entities:
            entity.draw()
        for state in self.state_machines:
            if True:                
                for box in state.current_state.hurt_boxes:
                    draw_bounding_box(box, GREEN)
        end_mode_3d()
    
    def save_state(self):
        self.saved_state.entities = self.game_state.entities
        self.saved_state.inputs = self.game_state.inputs
        self.saved_state.movement = self.game_state.movement
        self.saved_state.frame_count = self.game_state.frame_count
    
    def load_state(self):
        print("Loading State!!!")
        self.game_state.entities = self.saved_state.entities
        self.game_state.inputs = self.saved_state.inputs
        self.game_state.movement = self.saved_state.movement
        self.game_state.frame_count = self.saved_state.frame_count

    def check_round_over(self):
        for entity in self.entities:
            if entity.health == 0:
                entity.defeated = True
        
        if self.entities[0].defeated and self.entities[1].defeated:
            print("Both Entities defeated")
        elif self.entities[0].defeated and not self.entities[1].defeated:
            print("Player 1 Defeated")
        elif self.entities[1].defeated and not self.entities[0].defeated:
            print("Player 2 Defeated")
    
    def get_healthbar_width_percent(self,current_health: float, max_health: float, width: float) -> int:
        new_width = int(width * (current_health / max_health))
        return new_width if new_width > 0 else 0

    def show_match_hud(self):
        draw_rectangle_lines(50, 49, 250, 32, BLACK) #P1 Healthbar Outline
        draw_rectangle_lines(500, 49, 250, 32, BLACK) #P2Healthbar Outline
        draw_rectangle_pro(Rectangle(50,50,self.get_healthbar_width_percent(self.entities[0].health, self.entities[0].max_health, 250),30),Vector2(0,0), 0, RED)
        draw_rectangle_pro(Rectangle(250,50,self.get_healthbar_width_percent(self.entities[1].health, self.entities[1].max_health, 250),30),Vector2(500,30), 180, BLUE)
        draw_circle_lines(250,95,10,BLACK)
        draw_circle_lines(272,95,10,BLACK)
        draw_circle_lines(294,95,10,BLACK)
    
    def update_hit_events(self):
        for event in self.hit_events:
            defender_state: State = self.state_machines[event.defender_id].current_state
            attacker_on_left: bool = self.entities[event.defender_id].position.x < self.entities[event.attacker_id].position.x
            was_guarded: bool = False
            on_floor: bool = self.entities[event.defender_id].is_on_floor()

            if event.is_grab:
                if (self.entities[event.defender_id].is_on_floor() and self.entities[event.attacker_id].is_on_floor()) or (not self.entities[event.defender_id].is_on_floor() and not self.entities[event.attacker_id].is_on_floor()): #minimum height to grab should be determined by the attack and added to the hit event
                    self.state_machines[event.defender_id].change_state(self.state_machines[event.defender_id].get_state_by_id(117))
                    self.reaction_components[event.defender_id].grab_lock = True
            elif was_guarded:
                if self.entities[event.defender_id].is_on_floor() and self.entities[event.attacker_id].is_on_floor(): #Check if both entities are grounded
                    if self.state_machines[event.defender_id].current_state.state_id == 101: #Check if Standing
                                pass #Go to standing block stun state
                    elif self.state_machines[event.defender_id].current_state.state_id == 105: #Check if crouching
                                pass #Go to crouch block stun state  
                elif not self.entities[event.defender_id].is_on_floor() and not self.entities[event.attacker_id].is_on_floor(): #check if both entities are airbourne
                    pass #Go to air block stun state
                self.reaction_components[event.defender_id].guard_stun = event.guard_stun

            else:
                if event.is_launch:
                    if self.state_machines[event.defender_id].current_state.status == STATUS.STANDING:
                        self.reaction_components[event.defender_id].is_launch = event.is_launch
                        self.reaction_components[event.defender_id].air_knock_back = event.air_knock_back
                        self.reaction_components[event.defender_id].launch_velocity = event.launch_velocity
                        self.state_machines[event.defender_id].change_state(self.state_machines[event.defender_id].get_state_by_id(117))
                    elif self.state_machines[event.defender_id].current_state.status == STATUS.AIRBOURNE:
                        self.reaction_components[event.defender_id].is_launch = event.is_launch
                        self.reaction_components[event.defender_id].air_knock_back = event.air_knock_back
                        self.reaction_components[event.defender_id].launch_velocity = math.floor(event.launch_velocity/2)
                        self.state_machines[event.defender_id].change_state(self.state_machines[event.defender_id].get_state_by_id(117))
                elif event.is_knock_down:
                    pass
                else:
                    self.reaction_components[event.defender_id].knock_back = event.knock_back
                    match self.state_machines[event.defender_id].current_state.status:
                        case STATUS.STANDING:
                            if self.state_machines[event.defender_id].current_state.state_id == 101: #Check if Standing
                                pass #Go to standing stun state
                            elif self.state_machines[event.defender_id].current_state.state_id == 105: #Check if crouching
                                pass #Go to crouch stun state
                        case STATUS.AIRBOURNE:
                            pass #Go to air stun state                                    
                    pass
                self.reaction_components[event.defender_id].hit_stun = event.hit_stun
            for react in self.reaction_components:
                react.hit_stop = event.hit_stop
            self.last_hit_event = event
        self.hit_events.clear()
    
    def update_reactions(self):
        for reaction in self.reaction_components:
            if reaction.hit_stop > 0:
                reaction.hit_stop -= 1
            elif reaction.hit_stun > 0:
                reaction.hit_stun -= 1
                if reaction.hit_stun <= 0:
                    pass #Reset Combo counter and other related information
    
    def update_collisions(self):
        pushbox_a = BoundingBox(Vector3(self.entities[0].position.x - self.state_machines[0].current_state.push_box.min.x, self.entities[0].position.y - self.state_machines[0].current_state.push_box.min.y,1),
                                          Vector3(self.entities[0].position.x + self.state_machines[0].current_state.push_box.max.x,self.entities[0].position.y + self.state_machines[0].current_state.push_box.max.y,1))
        pushbox_b = BoundingBox(Vector3(self.entities[1].position.x - self.state_machines[1].current_state.push_box.min.x, self.entities[1].position.y - self.state_machines[1].current_state.push_box.min.y,1),
                                          Vector3(self.entities[1].position.x + self.state_machines[1].current_state.push_box.max.x,self.entities[1].position.y + self.state_machines[1].current_state.push_box.max.y,1))
        if check_collision_boxes(pushbox_a, pushbox_b):
            for move in self.movement_components:
                move.velocity.x -= 1 if move.facing_right else -1
        
        pass #Need to figure out where to store the hitboxes for each player
        #Something like
        #for hitbox in self.hitboxes[entity_id]:
        #      if check_collision_recs(hitbox, other_entity_hurtbox):
        #           add hit event 
        #           update has landed hit on entity 
        #           remove hitbox from lise
        #           break
        #   
        #

    def update_physics(self):
        #######DUE TO HOW ROLLBACK WORKS THESE VALUES NEED TO BE WHOLE NUMBERS#####
        knockback_decel: int = 5
        knockback_threshold: int = 10
        air_deceleration: int = 4
        for entity in  range(len(self.entities)):
            other_entity_x: float = self.movement_components[entity + 1 if entity +1 < len(self.entities) else 0].position.x
            facing_opponent: bool = (other_entity_x < self.movement_components[entity].position.x and not self.movement_components[entity].facing_right) or (other_entity_x > self.movement_components[entity].position.x and self.movement_components[entity].facing_right)
            if self.reaction_components[entity].hit_stop <= 0:
                if self.state_machines[entity].current_state.state_id == 110 or self.state_machines[entity].current_state.state_id == 111:
                    pass
                if (self.reaction_components[entity].hit_stun > 0 or self.reaction_components[entity].guard_stun > 0) and self.reaction_components[entity].knock_back != 0:
                    if self.reaction_components[entity].is_launch:
                        self.movement_components[entity].velocity.y = self.reaction_components[entity].launch_velocity
                        if self.movement_components[entity].facing_right:
                            self.movement_components[entity].velocity.x = -self.reaction_components[entity].air_knock_back
                        else:
                            self.movement_components[entity].velocity.x = self.reaction_components[entity].air_knock_back
                    else:
                        if self.movement_components[entity].facing_right:
                            self.movement_components[entity].velocity.x = -self.reaction_components[entity].knock_back
                        else:
                            self.movement_components[entity].velocity.x = self.reaction_components[entity].knock_back
                    
                    if self.state_machines[entity].current_state.state_id == 107 or self.state_machines[entity].current_state.state_id == 108:
                        self.reaction_components[entity].knock_back -= knockback_decel
                        if abs(self.reaction_components[entity].knock_back) <= knockback_threshold:
                            self.reaction_components[entity].knock_back = 0
                            self.movement_components[entity].velocity.x = 0
                    elif self.state_machines[entity].current_state.state_id == 118:
                        self.reaction_components[entity].air_knock_back -= knockback_decel
                        self.reaction_components[entity].launch_velocity = self.reaction_components[entity].launch_velocity - air_deceleration
            self.movement_components[entity].update()
            self.entities[entity].position = self.movement_components[entity].position


class NetMatchManager(MatchManager):
    def __init__(self, _net_type: NetworkType = NetworkType.HOST): #TODO Add in the Network Type to the Screen Manager so that it can pass that information to here
        super().__init__()
        self.host = None
        self.peer = None
        self.port = 1474
        self.entity_index: int = 0
        self.opponent_index: int = 1
        self.net_frame_input: InputCommand = InputCommand.NONE
        self.net_package: NetInputPackage = NetInputPackage()
        self.net_type:NetworkType = _net_type
        self.net_sync_type:NetSyncType = NetSyncType.ROLLBACK
        self.net_input_delay: int = 6
        self.latest_network_frame: int = -1
        self.MAX_ROLLBACK_FRAMES = 10
        self.received_net_input: bool = False

    def update(self):
        #Update input to use for this frame from the network
        self.input_history[self.entity_index] |= self.net_frame_input

        #Reset the input for the next frame
        self.net_frame_input = InputCommand.NONE

        #Poll for local input
        self.net_frame_input = self.input_components[self.entity_index].get_local_input()
        
        #Record this input in the buffer for sending to the other player
        if self.game_state.frame_count < self.INPUT_HISTORY_SIZE - self.net_input_delay:
            self.input_history[self.entity_index][self.game_state.frame_count + self.net_input_delay] = self.net_frame_input

        #Reset flag for receiving input from the network
        self.received_net_input = False

        #Send and receive input over the network
        self.network_update()

        if self.game_state.receivedNetInput:
            #Update the Network Input History
            StartFrame = self.game_state.netpackage.Frame-PACKET_HISTORY_SIZE+1
            for i in range(PACKET_HISTORY_SIZE):
                check_frame = StartFrame + i
                if check_frame == LastestNetworkFrame + 1:
                    LastestNetworkFrame += 1
                
                self.input_history[self.game_state.opponent_index][StartFrame+i] = self.game_state.netpackage.Input_History[i]

        #Should we update on the next frame?
        UpdateNextFrame = self.game_state.frame_count == 0


        if self.net_sync_type == NetSyncType.DELAY:
            #Only Update if we have the next frame of Input
            if LastestNetworkFrame >= self.game_state.frame_count:
                UpdateNextFrame = True
        elif self.net_sync_type == NetSyncType.ROLLBACK:
            #Limit how far ahead of the opponent we can get
            UpdateNextFrame = self.game_state.frame_count < LastestNetworkFrame + self.MAX_ROLLBACK_FRAMES-1

        if self.net_type == NetworkType.UNSET:
            UpdateNextFrame = False



        resimulating: bool = False
        #Frames to resimulate the game
        resim_frames: int = 1
        #Detect if we need to resumulate
        if LastestNetworkFrame > LastStoredFrame:
            resimulating = True
            UpdateNextFrame = True

            #Number of frames that need to be resimulated including the current frame
            resim_frames = self.game_state.frame_count - LastStoredFrame
            #Restore the Game State to the LastStoredFrame
            self.game_state.frame_count = self.saved_state.frame_count
            self.game_state.inputs = self.saved_state.inputs
            self.game_state.entities = self.saved_state.entities


        if UpdateNextFrame:
            SimFrame = 0
            for SimFrame in range(resim_frames): 
                #Assign Local player input
                self.game_state.inputs[self.game_state.entity_index] = self.input_history[self.game_state.entity_index][self.game_state.frame_count]
                #Assign Net player input
                self.game_state.inputs[self.game_state.opponent_index] = self.input_history[self.game_state.opponent_index][self.game_state.frame_count]
                
                #Update the simulation 

                UpdatePolledInput = True
                #update game frame
                self.game_state.frame_count +=1
                
                
                #Save Game State when we have input for that frame
                if resimulating:
                    if LastestNetworkFrame >= self.game_state.frame_count-1:
                        LastStoredFrame = self.game_state.frame_count - 1
                        print("Currently Storing inputs for frame: ", self.saved_state.frame_count, ". Current Game State Frame: ", self.game_state.frame_count)
                        self.saved_state.frame_count = self.game_state.frame_count
                        self.saved_state.inputs = self.game_state.inputs
                        self.saved_state.entities = self.game_state.entities
                        print("Current Frame after Storing Game State: ", self.saved_state.frame_count)
        #Update Camera Target
        self.camera.target = Vector3(0,50,0)
    
    def init_network(self, port):
        match self.net_type:
            case NetworkType.HOST:
                self.host = enet.Host(enet.Address(b"localhost", port),1,0,0,0) #Parameters: Address (IP, Port), Number of connections allowed, Channels, I don't remember the other 2
                self.entity_index = 0
                self.opponent_index = 1
            case NetworkType.CLIENT:
                self.host = enet.Host(None, 1,0,0,0)
                self.peer = self.host.connect(enet.Address(b"localhost", port), 1)
                self.entity_index = 1
                self.opponent_index = 0
        event = self.host.service(16)
        if event.type == enet.EVENT_TYPE_CONNECT:
            self.peer = event.peer


    def network_update(self):
        event = self.host.service(16)

        ToSendNetPackage: NetInputPackage = NetInputPackage()

        InputIndex = self.game_state.frame_count - PACKET_HISTORY_SIZE +1+self.net_input_delay

        for i in range(PACKET_HISTORY_SIZE):
            if InputIndex >= 0: #Make sure we aren't sending inputs for before the first frame of the game
                ToSendNetPackage.Input_History[i] = self.input_history[self.entity_index][InputIndex + i]
            else:
                ToSendNetPackage.Input_History[i] = InputCommand.NONE #Need a sentinal value instead of setting it to no input

        #Send inputs over Network
        self.peer.send(0,enet.Packet(pickle.dumps(ToSendNetPackage)))
                
        #Record inputs from Network
        if event.type == enet.EVENT_TYPE_RECEIVE:
            print("Received Message")
            info = pickle.loads(event.packet.data)
            print(info.Frame, info.Input_History)
            self.net_package.Frame = info.Frame
            for i in range(len(info.Input_History)):
                self.net_package.Input_History[i] = info.Input_History[i]
            self.received_net_input = True



    
