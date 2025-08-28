from pyray import *

class Entity:
    def __init__(self):
        self.health_pointer = ffi.new('float *', 1.0)
        self.max_health = 1.0
        self.health = self.max_health
        self.defeated: bool = False
        self.position: Vector3 = Vector3(0,50,0)
        self.velocity: Vector3 = Vector3(0,0,0)
        self.facing_right: bool = False
        self.gamepad_index: int = 0
        self.is_player_1: bool = True
    def draw(self):
        draw_cube(self.position, 100, 200,100,RED if self.is_player_1 == True else BLUE)
    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
    def is_on_floor(self)->bool:
        return self.position.y == 0

    
    