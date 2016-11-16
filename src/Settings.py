from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import platform
import sys

# sudo apt-get install python-matplotlib
#import matplotlib.pyplot as plt

class Settings(Widget):

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)

        win_w = Window.size[0]
        win_h = Window.size[1]

        self.Values = ['Background Image','Background Color','Header/Footer Image','Connection']
        self.Parent = None
        self.setmenu = DropDown()

        self.bibut = Button(text='Background Image', size_hint_y= None, height= 30)
        self.bibut.bind(on_release=self.bibutpress)
        self.setmenu.add_widget(self.bibut)

        self.bcbut = Button(text='Background Color', size_hint_y= None, height= 30)
        self.bcbut.bind(on_release=self.bcbutpress)
        self.setmenu.add_widget(self.bcbut)

        self.hfbut = Button(text='Header/Footer Color', size_hint_y= None, height= 30)
        self.hfbut.bind(on_release=self.hfbutpress)
        self.setmenu.add_widget(self.hfbut)

        self.conbut = Button(text='Connection', size_hint_y= None, height= 30)
        self.conbut.bind(on_release=self.conbutpress)
        self.setmenu.add_widget(self.conbut)

        self.rotbut = Button(text='Reset Rotations', size_hint_y=None, height = 30)
        self.rotbut.bind(on_release=self.rotbutpress)
        self.setmenu.add_widget(self.rotbut)

        self.exitbut = Button(text='Exit DigiDash', size_hint_y= None, height= 30)
        self.exitbut.bind(on_release=self.exitbutpress)
        self.setmenu.add_widget(self.exitbut)

        self.settingbutton = Button(text='Settings',size_hint=(None,None), size=(200,30)) 
        self.settingbutton.pos=(win_w-220,win_h-self.settingbutton.size[1])
        self.settingbutton.bind(on_release=self.setmenu.open)

        self.add_widget(self.settingbutton)

    def __resize__(instance):
        instance.settingbutton.pos=(win_w-220,win_h-self.settingbutton.size[1])
    def bibutpress(instance, *kwargs):
        print('The button <%s> is being pressed' % instance.bibut.text)
    def bcbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.bcbut.text)
    def hfbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.hfbut.text)
    def conbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.conbut.text)

	#plt.plot([1,2,3,4])
	#plt.ylabel('some numbers')
	#plt.show()

    def rotbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.rotbut.text)
        for ker in instance.Parent.ActiveGauges:
            ker.rotation = 0
    def set_parent(self, p):
        self.Parent = p
	#GraphClass.graph()
    def exitbutpress(instance, *largs):
        print('The button <%s> is being pressed' % instance.exitbut.text)
        App.get_running_app().stop()
	#sys.exit()

