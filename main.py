from pyray import *
from enum import Enum
from GameSettings import GameSettings as gs
from MatchManager import MatchManager
from ScreenManager import * 


class GameState:
    def __init__(self):
        self._game_settings = gs()
        self._screen_manager = ScreenManager(self._game_settings)

        
        self.run()
    def run(self):
        set_target_fps(60)
        
        while not window_should_close():
            self.update()
            self.draw()
        close_window()
    
    def update(self):
        self._screen_manager.update()
    
    def draw(self):
        begin_drawing()
        clear_background(RAYWHITE)
        self._screen_manager.draw_screen()
        end_drawing()


if __name__ == "__main__":
    _game_state = GameState()
