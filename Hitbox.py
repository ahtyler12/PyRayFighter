from HitEvent import HitEvent
from pyray import *
class Hitbox:
    def __init__(self, _rect: Rectangle, _hit_data: HitEvent):
        self.hit_data: HitEvent = _hit_data
        self.rect: Rectangle = _rect