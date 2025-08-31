from pyray import *
from enum import Enum
from GameSettings import GameSettings as gs
from MatchManager import MatchManager
from ScreenManager import * 
from ImguiRenderer import ImguiRenderer
class GameState:
    def __init__(self):
        self._game_settings = gs()
        self._screen_manager = ScreenManager(self._game_settings)
        self.imgui_render = ImguiRenderer()


        
        self.run()
    def run(self):
        set_target_fps(60)
        
        
        
        while not window_should_close():
            self.update()
            self.draw()
        self.imgui_render.backend.shutdown()
        close_window()
    
    def update(self):
        self.imgui_render.update()
        self._screen_manager.update()
    
    def draw(self):
        begin_drawing()
        clear_background(RAYWHITE)
        self._screen_manager.draw_screen()
        rl_draw_render_batch_active()
        self.imgui_render.draw()
        end_drawing()


if __name__ == "__main__":
    _game_state = GameState()
