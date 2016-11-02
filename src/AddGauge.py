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


class AddGauge(Widget):

    def __init__(self, **kwargs):
        super(AddGauge, self).__init__(**kwargs)

        #REF TO PARENT CLASS
        self.Parent = None
    
        self.Values= ['Engine Load',
                 'Fuel Pressure',
                 'Tachometer',
                'Speedometer',
                'MAF',
                'Throttle Pos',
                'Boost Pressure']


        self.codetype = DropDown()

        for x in self.Values:
            cur = Button(text=x, size_hint_y= None, height= 40)
            self.codetype.add_widget(cur)
            
        self.mainbutton = Button(text='New Gauge', size_hint=(None,None), size=(200,40), pos=(20,550))
        self.mainbutton.bind(on_release=self.codetype.open)
        self.add_widget(self.mainbutton)

    def set_parent(self,p):
        self.Parent = p



