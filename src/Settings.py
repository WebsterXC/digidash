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

        self.bcbut = Button(text='Brightness', size_hint_y= None, height= 30)
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
        def imgbut0press(instance,*largs):
            par.bg.source='Images/Metal.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut0.text)
        def imgbut1press(instance,*largs):
            par.bg.source='Images/Metal2.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut1.text)
        def imgbut2press(instance,*largs):
            par.bg.source='Images/bgcblue.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut2.text)
        def imgbut3press(instance,*largs):
            par.bg.source='Images/bgcblack.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut3.text)
        def imgbut4press(instance,*largs):
            par.bg.source='Images/bgcred.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut4.text)
        def imgbut5press(instance,*largs):
            par.bg.source='Images/bgcyellow.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut5.text)
        def imgbut6press(instance,*largs):
            par.bg.source='Images/bgcgreen.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut6.text)
        def imgbut7press(instance,*largs):
            par.bg.source='Images/bgcwhite.jpg'
            sm.remove_widget(imgbut0)
            sm.remove_widget(imgbut1)
            sm.remove_widget(imgbut2)
            sm.remove_widget(imgbut3)
            sm.remove_widget(imgbut4)
            sm.remove_widget(imgbut5)
            sm.remove_widget(imgbut6)
            sm.remove_widget(imgbut7)
            sm.add_widget(bi)
            sm.add_widget(bc)
            sm.add_widget(hf)
            sm.add_widget(con)
            sm.add_widget(rot)
            sm.add_widget(ex)
            print('The button <%s> is being pressed' % imgbut7.text)
            
        print('The button <%s> is being pressed' % instance.bibut.text)
        par = instance.Parent
        sm = instance.setmenu
        bi = instance.bibut
        bc = instance.bcbut
        hf = instance.hfbut
        con = instance.conbut
        rot = instance.rotbut
        ex = instance.exitbut
        #instance.Parent.bg.source='Images/Metal.jpg'
        instance.setmenu.remove_widget(instance.bibut)
        instance.setmenu.remove_widget(instance.bcbut)
        instance.setmenu.remove_widget(instance.hfbut)
        instance.setmenu.remove_widget(instance.conbut)
        instance.setmenu.remove_widget(instance.rotbut)
        instance.setmenu.remove_widget(instance.exitbut)
        imgbut0 = Button(text='Metal 1', size_hint_y= None, height= 30)
        imgbut0.bind(on_release=imgbut0press)
        imgbut1 = Button(text='Metal 2', size_hint_y= None, height= 30)
        imgbut1.bind(on_release=imgbut1press)
        imgbut2 = Button(text='Blue', size_hint_y= None, height= 30)
        imgbut2.bind(on_release=imgbut2press)
        imgbut3 = Button(text='Black', size_hint_y= None, height= 30)
        imgbut3.bind(on_release=imgbut3press)
        imgbut4 = Button(text='Red', size_hint_y= None, height= 30)
        imgbut4.bind(on_release=imgbut4press)
        imgbut5 = Button(text='Yellow', size_hint_y= None, height= 30)
        imgbut5.bind(on_release=imgbut5press)
        imgbut6 = Button(text='Green', size_hint_y= None, height= 30)
        imgbut6.bind(on_release=imgbut6press)
        imgbut7 = Button(text='White', size_hint_y= None, height= 30)
        imgbut7.bind(on_release=imgbut7press)
        instance.setmenu.add_widget(imgbut0)
        instance.setmenu.add_widget(imgbut1)
        instance.setmenu.add_widget(imgbut2)
        instance.setmenu.add_widget(imgbut3)
            
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