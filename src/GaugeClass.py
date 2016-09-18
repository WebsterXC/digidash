from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.clock import Clock
import time


class Gauge(Widget):
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        self.gauge = Image(source='Images/Guage_Big.png', size=(400,400))
        
        self.dialscat = Scatter()
        self.dialscat.center = self.gauge.center
        self.dial = Image(source='Images/dial.png',size=(300,300), pos=(-105,-90))
        self.dialscat.add_widget(self.dial)
        self.dialscat.rotation = 1

        
        self.add_widget(self.gauge)
        self.add_widget(self.dialscat)
        self.size=self.gauge.size

    def setMPH(self, mph):
        angle = 360-(1.3655*mph)
        self.dialscat.rotation=angle
        
    def MPH2Angle(self, mph):
        return (1.3655*mph)
        
    def on_touch_down(self, touch):
        angle = Gauge.MPH2Angle(self,80)
        anim = Animation(rotation=-angle, duration=6.)
        anim.start(self.dialscat)
    
        


    
