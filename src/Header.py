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
import platform


class Header(Widget):

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)

        win_w = Window.size[0]
        win_h = Window.size[1]

        if(platform.platform()=='Linux-4.1.19-v7+-armv7l-with-Ubuntu-16.04-xenial'):
            win_h= 480

        self.bg = Image(source='Images/StatusBar.png', size=(win_w,win_h/12), pos=(0,win_h-60))
        self.add_widget(self.bg)
        
        self.size = self.bg.size
