from pyray import *

class MovementComponent:
    def __init__(self):
        self.position: Vector3 = Vector3(0,50,0)
        self.velocity: Vector3 = Vector3(0,0,0)
        self.facing_right: bool = False
    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
    def is_on_floor(self)->bool:
        return self.position.y == 0