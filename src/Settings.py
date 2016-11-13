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
import sys
import GraphClass


class Settings(Widget):

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        win_w = Window.size[0]
        win_h = Window.size[1]
        if(platform.platform()=='Linux-4.1.19-v7+-armv7l-with-Ubuntu-16.04-xenial'):
            win_h= 480

        self.Values = ['Background Image','Background Color','Header/Footer Image','Connection']

        self.setmenu = DropDown()

        self.bibut = Button(text='Background Image', size_hint_y= None, height= 20)
        self.bibut.bind(on_release=self.bibutpress)
        self.setmenu.add_widget(self.bibut)

        self.bcbut = Button(text='Background Color', size_hint_y= None, height= 20)
        self.bcbut.bind(on_release=self.bcbutpress)
        self.setmenu.add_widget(self.bcbut)

        self.hfbut = Button(text='Header/Footer Color', size_hint_y= None, height= 20)
        self.hfbut.bind(on_release=self.hfbutpress)
        self.setmenu.add_widget(self.hfbut)

        self.conbut = Button(text='Connection', size_hint_y= None, height= 20)
        self.conbut.bind(on_release=self.conbutpress)
        self.setmenu.add_widget(self.conbut)

        self.exitbut = Button(text='Exit DigiDash', size_hint_y= None, height= 20)
        self.exitbut.bind(on_release=self.exitbutpress)
        self.setmenu.add_widget(self.exitbut)

        self.settingbutton = Button(text='Settings',size_hint=(None,None), size=(200,20), pos=(win_w-220,win_h-55))
        self.settingbutton.bind(on_release=self.setmenu.open)

        self.add_widget(self.settingbutton)

    def bibutpress(instance, *kwargs):
        print('The button <%s> is being pressed' % instance.bibut.text)
    def bcbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.bcbut.text)
    def hfbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.hfbut.text)
    def conbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.conbut.text)
	GraphClass.graph()
    def exitbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.exitbut.text)
        App.get_running_app().stop()
	#sys.exit()

