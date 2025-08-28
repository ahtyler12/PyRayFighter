from enum import Enum

class HITLEVEL(Enum):
    HIGH = 0
    MID = 1
    LOW = 2

class KND_TYPE(Enum):
    NONE = 0
    SOFT = 1
    HARD = 2

class HitEvent:
    event_id:int = 0
    attacker_id:int = 0
    defender_id:int = 0
    active_frame:int = 0
    frame_duration:int = 0
    hit_stun: int = 0
    hit_stop: int = 0
    guard_stun: int = 0
    knock_back: int = 0
    air_knock_back: int = 0
    launch_velocity: int = 0
    attack_has_hit: bool = False
    can_special_cancel: bool = False
    is_launch: bool = False
    is_grab: bool = False
    grab_lock: bool = False
    is_knock_down: bool = False
    knock_down_type: KND_TYPE = KND_TYPE.NONE
    is_ground_bounce: bool = False
    is_wall_bounce: bool = False
    damage: int = 0
    min_scaling: float = 1.0
    hit_level: HITLEVEL = HITLEVEL.HIGH
    x_offset: float = 0.0
    y_offset: float = 0.0
    x_size: float = 0.0
    y_size: float = 0.0
