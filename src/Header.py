from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.clock import Clock
import time


class Header(Widget):

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.bg = Image(source='Images/StatusBar.png', pos=(0,530), size=(800,80))
        self.add_widget(self.bg)   
        self.blutooth = Image(source='Images/blutooth.png', pos=(580,15), size=(50,55))
        self.add_widget(self.blutooth)
        self.size = self.bg.size






    
        
