from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
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






        self.add_widget(self.bg)
        self.drop = Header.genDropdown(self)
        self.add_widget(self.drop)
        self.blutooth = Image(source='Images/blutooth.png', pos=(580,15), size=(50,55))
        self.add_widget(self.blutooth)
        self.connectbtn = Button(text='CONNECT', width =160, height=40, pos=(630,20))
        self.add_widget(self.connectbtn)
        self.size = self.bg.size


    def genDropdown(self):
        """
            Fuction to be used to add possible gauge values from file.
        """
        Values= ['Calculated Engine Load',
                 'Fuel Pressure',
                 'Engine RPM',
                 'Vehicle Speed',
                 'MAF air flow rate',
                 'Throttle position',]

        codetype = DropDown()

        for x in Values:
            cur = Button(text=x, height=40, width=250)
            codetype.add_widget(cur)

        mainbutton = Button(text='Add New Gauge', height=40, width=250, pos=(20,20))
        mainbutton.bind(on_release=codetype.open)
        codetype.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        
        return mainbutton            
    
        
