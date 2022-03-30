'''                                                                                                                         
Application built from a  .kv file                                                                                          
==================================                                                                                          
                                                                                                                            
This shows how to implicitly use a .kv file for your application. You                                                       
should see a full screen button labelled "Hello from test.kv".                                                              
                                                                                                                            
After Kivy instantiates a subclass of App, it implicitly searches for a .kv                                                 
file. The file test.kv is selected because the name of the subclass of App is                                               
TestApp, which implies that kivy should try to load "test.kv". That file                                                    
contains a root Widget.                                                                                                     
'''                                                                                                                         
                                                                                                                            
import kivy                                                                                                                 
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import DictProperty
from printer import Printer
kivy.require('1.0.7')                                                                                                       
                                                                                                                            
from kivy.app import App                                                                                                    

printer = Printer('/dev/ttyUSB0', 250000)
                                                                                                                            
TOP_X         =  250
BOTTOM_X      =  50
TOP_Y         =  250
BOTTOM_Y      =  10
TOP_Z         =  5
BOTTOM_Z      =  0

class Slider_pos(BoxLayout):
    __events__ =  ('on_press',)

    def on_press(self, *largs):
        move = self.ids['slider_display'].text

        if self.ids['btn'].text == 'X':
            printer.move_x_absolute(move)
        elif self.ids['btn'].text == 'Y':
            printer.move_y_absolute(move)
        elif self.ids['btn'].text == 'Z':
            printer.move_z_absolute(move)
        elif self.ids['btn'].text == 'E':
            printer.move_extruder(move)
        elif self.ids['btn'].text == 'FeedRate':
            printer.set_feedrate(move)
        elif self.ids['btn'].text == 'Nozzle':
            printer.set_nozzle_temp(move)
        elif self.ids['btn'].text == 'Bed':
            printer.set_bed_temp(move)

class GuiPrinter(Screen, BoxLayout):                                                                                                

    def btn(self):                                                                                                          
        print("General function")                                                                                           
                                                                                                                            
    def btn_left_back(self):                                                                                                
        printer.move_z_absolute(TOP_Z)
        printer.move_x_absolute(BOTTOM_X)
        printer.move_y_absolute(TOP_Y)
        printer.move_z_absolute(BOTTOM_Z)
                                                                                                                            
    def btn_left_front(self):                                                                                               
        printer.move_z_absolute(TOP_Z)
        printer.move_x_absolute(BOTTOM_X)
        printer.move_y_absolute(BOTTOM_Y)
        printer.move_z_absolute(BOTTOM_Z)
        print("Left front")                                                                                                 
        self.btn()                                                                                                          
                                                                                                                            
    def btn_right_back(self):                                                                                               
        printer.move_z_absolute(TOP_Z)
        printer.move_x_absolute(TOP_X)
        printer.move_y_absolute(TOP_Y)
        printer.move_z_absolute(BOTTOM_Z)
        print("Right back")                                                                                                 
        self.btn()                                                                                                          
                                                                                                                            
    def btn_right_front(self):                                                                                              
        printer.move_z_absolute(TOP_Z)
        printer.move_x_absolute(TOP_X)
        printer.move_y_absolute(BOTTOM_Y)
        printer.move_z_absolute(BOTTOM_Z)
        print("Right front")                                                                                                
        self.btn()                                                                                                          

    def btn_home(self):
        print("go home")
        printer.home()
                                                                                                                                    
class Temperature_Widget(BoxLayout):
    __events__ =  ('on_press',)

    def on_press(self, *largs):
        move = self.ids['slider_display'].text

        if self.ids['btn'].text == 'X':
            printer.move_x_absolute(move)
        elif self.ids['btn'].text == 'Y':
            printer.move_y_absolute(move)
        elif self.ids['btn'].text == 'Z':
            printer.move_z_absolute(move)
        elif self.ids['btn'].text == 'Nozzle':
            printer.set_nozzle_temp(move)
        elif self.ids['btn'].text == 'Bed':
            printer.set_bed_temp(move)

class SettingsScreen(Screen):
    temperature = DictProperty({"nozzle": 0, "bed": 0})

    def temperature_display(self, dt):
        (nozzle, bed) = printer.get_temp()
        if (nozzle != 0 or bed != 0):
            self.temperature["nozzle"] = round(float(nozzle))
            self.temperature["bed"] = round(float(bed))

class ExtrusionScreen(Screen):
    pass

class TestApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        gui_printer = GuiPrinter(name='main_view')
        settings_screen = SettingsScreen(name='settings')
        extrusion_screen = ExtrusionScreen(name='extrusion')
        sm.add_widget(gui_printer)
        sm.add_widget(settings_screen)
        sm.add_widget(extrusion_screen)
        Clock.schedule_interval(settings_screen.temperature_display, 3)

        return sm

if __name__ == '__main__':
    TestApp().run()
