from imgui_bundle import imgui
from imgui_bundle.python_backends.opengl_backend_programmable import ProgrammablePipelineRenderer
from imgui_integration import init_imgui
from pyray import *

class ImguiRenderer:
    def __init__(self):
        imgui.create_context()
        self.backend = ProgrammablePipelineRenderer()
        self.backend.io.display_size = imgui.ImVec2(get_screen_width(),
                                      get_screen_height())
    
    def update(self):       
        self.backend.process_inputs()
    

    def draw(self):
        imgui.new_frame()
        imgui.begin("Hello, world!")
        imgui.text("This is some useful text. :p")
        if imgui.button("Click me!"):
         counter += 1
        imgui.end()
        imgui.render()
        self.backend.render(imgui.get_draw_data())

    #TODO create function to make windows for specific data