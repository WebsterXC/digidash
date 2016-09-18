from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock
from kivy.app import App
import time


class Footer(Widget):
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)
        self.bg = Image(source='Images/StatusBar.png', size=(800,80))
        self.title = Label(text='DigiDash', font_size='60sp', pos=(380,-10))
        #print(self.title.size)
        self.date = Label(text='Friday, September 16th 2016', font_size='18sp', pos=(75,-10))
        #print(self.date.size)
        self.time = Label(text='12:00:00 EST', font_size='24sp', pos=(650,-10))
        #print(self.time.size)

        self.add_widget(self.bg)
        self.add_widget(self.title)
        self.add_widget(self.date)
        self.add_widget(self.time)

        self.size = self.bg.size
        #print(self.size)
        #print(self.bg.size)

    def updatetime(self, *largs):
        self.time.text= time.strftime("%H:%M:%S") + ' EST'
        #print(time.strftime("%H:%M:%S"))

    def updatedate(self, *largs):
        self.date.text= time.strftime("%A, %B %d %Y")
        
        

        
        


        
    
        
