class ReactionComponent:
    def __init__(self):
        self.hit_stun: int = 0
        self.guard_stun: int = 0
        self.hit_stop: int = 0
        self.knock_back: int = 0
        self.air_knock_back: int = 0
        self.launch_velocity: int = 0
        self.attack_has_hit: bool = False
        self.attack_can_special_cancel: bool = False
        self.is_launch: bool = False
        self.is_grab: bool = False
        self.grab_lock: bool = False