from enum import Enum
from pyray import *
from GameSettings import *
from MatchManager import MatchManager
import ctypes
import enet #May need to move this to an actual Online Mode File



class SCREEN(Enum):
    LOGO = 0
    MAINMENU =1
    SETTINGS = 2
    ONLINE = 3
    CHARACTERSELECT = 4
    MATCH = 5

class ScreenManager:
    def __init__(self, _new_settings: GameSettings):
        self.current_screen = SCREEN.MATCH
        self.settings = _new_settings
        self.main_menu_button_index: int = 0
        self.main_menu_max_button_index: int = 1
        self.remember: bool = False #Should be set from settings. Here for now
        self._match_manager = None
        self.temp_sound = ffi.new('float *', 1.0)
        self.show_debug: bool = False
        self.rect_height: float = 50
        self.rect_width: float = 300
        self.main_offline_rect: Rectangle = (0,0,self.rect_width,self.rect_height)
        self.main_online_rect: Rectangle = (0,0,self.rect_width,self.rect_height)
        self.main_settings_rect: Rectangle = (0,0,self.rect_width,self.rect_height)
        self.main_quit_rect: Rectangle = (0,0,self.rect_width,self.rect_height)


        




    def change_screen(self, _new_screen: SCREEN):
        self.current_screen = SCREEN.MAINMENU
        match _new_screen:
            case SCREEN.LOGO:
                if self.current_screen == SCREEN.MAINMENU:
                    return SCREEN.LOGO
            case SCREEN.MAINMENU:
                if self.current_screen != SCREEN.CHARACTERSELECT:
                    if not self.remember:
                        self.main_menu_button_index = 0
                    return SCREEN.MAINMENU
            case SCREEN.SETTINGS:
                if self.current_screen != SCREEN.ONLINE:
                    return SCREEN.SETTINGS
            case SCREEN.ONLINE:
                return SCREEN.ONLINE
            case SCREEN.CHARACTERSELECT:
                return SCREEN.CHARACTERSELECT
            case SCREEN.MATCH:                
                self._match_manager = MatchManager()
                return SCREEN.MATCH

    

    def draw_logo(self):   
        draw_text("Insert Logo Here", 400, 300, 36, BLACK)
        if is_key_pressed(self.settings.menu_accept):
            self.settings.save_settings()
        if gui_button(Rectangle(300,300,300,30), "Main Menu") != 0:
            self.change_screen(SCREEN.MAINMENU)
        if gui_button(Rectangle(300,350, 300,30), "Load Settings"):
            self.settings.load_settings()
        
        if gui_slider_bar(Rectangle(300,400,300,30), "","", self.temp_sound, 0.0, 1.0):
            self.settings._sound_settings.set_master(round(self.temp_sound[0], 2))
        
 
        

    def draw_main_menu(self):
        main_menu_left: float = get_screen_width()*.15
        main_menu_right: float = get_screen_width()*.85
        main_menu_top: float = get_screen_height() * .25
        main_menu_bottom: float = get_screen_height() * .75
        draw_text("Main Menu", int(main_menu_left), int(main_menu_top), 36, BLACK)
        if gui_button(Rectangle(main_menu_left,main_menu_top + 50,300,50), "Offline"):
            pass #No Offline Menus to show just yet
        if gui_button(Rectangle(main_menu_left,main_menu_top + 105,300,50), "Online"):
            self.change_screen(SCREEN.ONLINE)
       
    def draw_settings(self):
       draw_text("Settings", 400, 300, 36, BLACK)
       
    
    def draw_online(self):
        draw_text("Online", 400, 300, 36, BLACK)
    def draw_character_select(self):
        draw_text("Character Select", 400, 300, 36, BLACK)
   
    def draw_match_screen(self):

        #draw_text("Match", 400, 300, 36, BLACK)
        if self._match_manager is None:
            self._match_manager = MatchManager()
            self._match_manager.draw()
        else:
            self._match_manager.draw()


    def draw_screen(self): 
        if self.show_debug:
            self.show_debug_screen()
        match self.current_screen:
            case SCREEN.LOGO:
                self.draw_logo()
            case SCREEN.MAINMENU:
                self.draw_main_menu()
            case SCREEN.SETTINGS:
                self.draw_settings()
            case SCREEN.ONLINE:
                self.draw_online()
            case SCREEN.CHARACTERSELECT:
                self.draw_character_select()
            case SCREEN.MATCH:
                self.draw_match_screen()
    
    def update(self):
        match self.current_screen:
            case SCREEN.LOGO:
                self.update_logo()
            case SCREEN.MAINMENU:
                self.update_main_menu()
            case SCREEN.SETTINGS:
                self.update_settings()
            case SCREEN.ONLINE:
                self.update_online()
            case SCREEN.CHARACTERSELECT:
                self.update_character_select()
            case SCREEN.MATCH:
                self.update_match_screen()

    def update_logo(self):
        pass
        # for key in KeyboardKey:
        #     if is_key_pressed(key):
        #         self.change_screen(SCREEN.MAINMENU)
    
    def update_main_menu(self):
        if GameSettings.menu_up and self.main_menu_button_index <= self.main_menu_max_button_index:
            self.main_menu_max_button_index -= 1
        
        if GameSettings.menu_down and self.main_menu_button_index >= 0:
            self.main_menu_max_button_index += 1
        

    def update_settings(self):
        pass

    def update_online(self):
        pass
    def update_match_screen(self):
        if self._match_manager is not None:
            self._match_manager.update()
    
    def update_character_select(self):
        pass
    
    def show_debug_screen(self):
        match self.current_screen:
            case SCREEN.LOGO:
                self.update_logo()
            case SCREEN.MAINMENU:
                self.update_main_menu()
            case SCREEN.SETTINGS:
                self.update_settings()
            case SCREEN.ONLINE:
                self.update_online()
            case SCREEN.CHARACTERSELECT:
                self.update_character_select()
            case SCREEN.MATCH:
                self.update_match_screen()
        
        
    def print_me(sender):
        print(f"Menu Item: {sender}")
    def go_to_main(self):
        self.change_screen(SCREEN.MAINMENU)
        print("Going to Main")