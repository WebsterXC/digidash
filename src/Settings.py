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


class Settings(Widget):

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        
        self.Values = ['Background Image','Background Color','Header/Footer Image','Connection']
        
        self.setmenu = DropDown()
        
        self.bibut = Button(text='Background Image', size_hint_y= None, height= 40)
        self.bibut.bind(on_release=self.bibutpress)
        self.setmenu.add_widget(self.bibut)
        
        self.bcbut = Button(text='Background Color', size_hint_y= None, height= 40)
        self.bcbut.bind(on_release=self.bcbutpress)
        self.setmenu.add_widget(self.bcbut)
        
        self.hfbut = Button(text='Header/Footer Color', size_hint_y= None, height= 40)
        self.hfbut.bind(on_release=self.hfbutpress)
        self.setmenu.add_widget(self.hfbut)
        
        self.conbut = Button(text='Connection', size_hint_y= None, height= 40)
        self.conbut.bind(on_release=self.conbutpress)
        self.setmenu.add_widget(self.conbut)
        
        
        self.settingbutton = Button(text='Settings',size_hint=(None,None), size= (200,40), pos=(580,550))
        self.settingbutton.bind(on_release=self.setmenu.open)
        
        self.add_widget(self.settingbutton)
        
    def bibutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.bibut.text)
    def bcbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.bcbut.text)
    def hfbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.hfbut.text)
    def conbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.conbut.text)