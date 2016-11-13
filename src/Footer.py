from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
import time


class Footer(Widget):
    def __init__(self, **kwargs):
        super(Footer, self).__init__(**kwargs)
        win_w = Window.size[0]
        win_h = Window.size[1]

        self.bg = Image(source='Images/StatusBar.png', size=(win_w,win_h/12), pos=(0,-10))
        self.title = Label(text='DigiDash', font_size='46sp', pos=((win_w/2)-20,-25))
        #print(self.title.size)
        self.date = Label(text='Friday, September 16th 2016', font_size='18sp', pos=(85,-35))
        #print(self.date.size)
        self.time = Label(text='12:00:00 EST', font_size='20sp', pos=(win_w-140,-35))
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

    def __resize__(self, inst):
        self.bg.size=(win_w,win_h/12)
        self.bg.pos=pos=(0,-10)
