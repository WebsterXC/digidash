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


class AddGauge(Widget):

    def __init__(self, **kwargs):
        super(AddGauge, self).__init__(**kwargs)

        win_w = Window.size[0]
        win_h = Window.size[1]
        if(platform.platform()=='Linux-4.1.19-v7+-armv7l-with-Ubuntu-16.04-xenial'):
            win_h= 480

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
            cur = Button(text=x, size_hint_y= None, height= 30)
            self.codetype.add_widget(cur)

        self.mainbutton = Button(text='New Gauge', size_hint=(None,None), size=(200,30))
        self.mainbutton.pos=(20,win_h-self.mainbutton.size[1])
        self.mainbutton.bind(on_release=self.codetype.open)
        self.add_widget(self.mainbutton)

    def __resize__(instance):
        instance.mainbutton.pos=(20,win_h-self.mainbutton.size[1])

    def set_parent(self,p):
        self.Parent = p
