from pyray import *
from enum import Enum
import json

class SoundSettings:
    def __init__(self):
        self.master_volume = 1.0
        self.data = {
            "master_volume" : self.master_volume
        }
        
    def GetMaster(self):
        return get_master_volume()
    def set_master(self, new_volume: float):
        set_master_volume(new_volume)
        self.master_volume = new_volume
    def write_sound_settings(self):
        pass
    def read_sound_settings():
        pass

class MatchSettings:
    def __init__(self):
        self.num_rounds = 2
        self.round_time = 99.0
    def set_round_count(self, _new_rounds: int):
        self.num_rounds = _new_rounds
    def set_round_time(self, _new_round_time: float):
        self.round_time = _new_round_time
    def get_round_time(self):
        return self.round_time
    def get_round_count(self):
        return self.num_rounds
    def write_match_settings(self):
        pass
    def read_match_settings(self):
        pass

class ScreenMode(Enum):
    WINDOWED = 1
    BORDERLESS = 2
    FULLSCREEN = 3

class VideoSettings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen_mode = ScreenMode.WINDOWED
        self.data = {
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "screen_mode": self.screen_mode.value
        }
    def init_video(self):
        self.update_screen_mode(ScreenMode.WINDOWED)
    def init_screen_mode(self, _new_mode: ScreenMode):
        self.screen_mode = _new_mode
    def get_screen_height(self):
        return self.screen_height
    def get_screen_width(self):
        return self.screen_width
    def set_screen_height(self, _new_height: float):
        self.screen_height = _new_height
    def set_screen_width(self, _new_width: float):
        self.screen_width = _new_width
    def get_screen_mode(self):
        return self.screen_mode
    def update_screen_mode(self,_new_mode: ScreenMode):
        match _new_mode:
            case ScreenMode.WINDOWED:
                init_window(self.screen_width, self.screen_height, "RAYLIB")
            case ScreenMode.BORDERLESS:
                init_window(self.screen_width, self.screen_height, "RAYLIB")
                toggle_borderless_windowed()
            case ScreenMode.FULLSCREEN:
                init_window(self.screen_width, self.screen_height, "RAYLIB")
                toggle_fullscreen()
            case _:
                init_window(self.screen_width, self.screen_height, "RAYLIB")
        self.screen_mode = _new_mode
    def print_video_settings(self):
        print(self.data)
    def load_video_settings(self, _new_settings: dict):
        print(_new_settings)
        self.screen_width = _new_settings['screen_width']
        self.screen_height = _new_settings['screen_height']
        self.screen_mode = ScreenMode(_new_settings['screen_mode'])
        self.print_video_settings()
    


class GameSettings:
    should_close: bool = False
    menu_up: KeyboardKey = KeyboardKey.KEY_UP
    menu_down: KeyboardKey = KeyboardKey.KEY_DOWN
    menu_left:KeyboardKey  = KeyboardKey.KEY_LEFT
    menu_right: KeyboardKey = KeyboardKey.KEY_RIGHT
    menu_accept: KeyboardKey = KeyboardKey.KEY_ENTER
    menu_cancel: KeyboardKey = KeyboardKey.KEY_BACKSLASH


    def __init__(self):
        self.should_close: bool = False
        self._sound_settings = SoundSettings()
        self._match_settings = MatchSettings()
        self._video_settings = VideoSettings()
        self._video_settings.init_video()
        self._settings: dict = dict()
    def save_settings(self):
        self._settings['Video Settings'] = self._video_settings.data
        self._settings['Sound Settings'] = self._sound_settings.data
        with open('GameSettings.json', 'w+') as f:
            json.dump(self._settings, f, indent=2)

    def print_settings(self):
        self._video_settings.print_video_settings()
    def load_settings(self):
        with open('GameSettings.json', 'r') as f:
            self._settings = json.load(f)
            self._video_settings.load_video_settings(self._settings['Video Settings'])




