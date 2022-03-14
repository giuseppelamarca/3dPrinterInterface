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
from kivy.uix.boxlayout import BoxLayout
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

class GuiPrinter(BoxLayout):                                                                                                

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
                                                                                                                                    
class TestApp(App):                                                                                                         
    pass                                                                                                                    
                                                                                                                            
                                                                                                                            
if __name__ == '__main__':                                                                                                  
    TestApp().run() 
