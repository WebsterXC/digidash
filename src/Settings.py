from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from functools import partial
import platform
import sys
import subprocess
import ConfigParser

# sudo apt-get install python-matplotlib
#import matplotlib.pyplot as plt

class Settings(Widget):
    
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        
        global Config
        Config = ConfigParser.ConfigParser()
        Config.read("Settings.ini")
        
        win_w = Window.size[0]
        win_h = Window.size[1]

        #self.Values = ['Background Image','Background Color','Header/Footer Image','Connection']
        self.Parent = None
        self.setmenu = DropDown()

        self.imagebuttons = []
        self.brightbuttons = []

        self.bibut = Button(text='BACKGROUND IMAGE', size_hint_y= None, height= 30)
        self.bibut.bind(on_release=self.bibutpress)
        self.setmenu.add_widget(self.bibut)

        self.bcbut = Button(text='BRIGHTNESS', size_hint_y= None, height= 30)
        self.bcbut.bind(on_release=self.bcbutpress)
        self.setmenu.add_widget(self.bcbut)

        #self.hfbut = Button(text='Header/Footer Color', size_hint_y= None, height= 30)
        #self.hfbut.bind(on_release=self.hfbutpress)
        #self.setmenu.add_widget(self.hfbut)

        #self.conbut = Button(text='Connection', size_hint_y= None, height= 30)
        #self.conbut.bind(on_release=self.conbutpress)
        #self.setmenu.add_widget(self.conbut)

        self.rotbut = Button(text='RESET ROTATIONS', size_hint_y=None, height = 30)
        self.rotbut.bind(on_release=self.rotbutpress)
        self.setmenu.add_widget(self.rotbut)

        self.exitbut = Button(text='[   EXIT   ]', size_hint_y= None, height= 30, color=(1, 0, 0, 1))
        self.exitbut.bind(on_release=self.exitbutpress)
        self.setmenu.add_widget(self.exitbut)

        self.settingbutton = Button(text='Settings',size_hint=(None,None), size=(200,30)) 
        self.settingbutton.pos=(win_w-220,win_h-self.settingbutton.size[1])
        self.settingbutton.bind(on_release=self.setmenu.open)

        self.add_widget(self.settingbutton)
        
    def __resize__(instance):
        instance.settingbutton.pos=(win_w-220,win_h-self.settingbutton.size[1])
        
    def imgbutpress(instance, sourceimg, *largs):
            if sourceimg != 'none':
                instance.Parent.bg.source=str(sourceimg)
                Config.set('Application_Settings','Background',sourceimg)
                with open('Settings.ini', 'wb') as configfile:
                    Config.write(configfile)
            
            for but in instance.imagebuttons:
                instance.setmenu.remove_widget(but)
            
            instance.setmenu.add_widget(instance.bibut)
            instance.setmenu.add_widget(instance.bcbut)
            #instance.setmenu.add_widget(instance.hfbut)
            #instance.setmenu.add_widget(instance.conbut)
            instance.setmenu.add_widget(instance.rotbut)
            instance.setmenu.add_widget(instance.exitbut)
    
    def brightbutpress(instance, brightstr, *largs):
        if brightstr != 'back':
            subprocess.call(['sudo','./brightness.sh',str(brightstr)])
			
        for but in instance.brightbuttons:
                instance.setmenu.remove_widget(but)
    
        instance.setmenu.add_widget(instance.bibut)
        instance.setmenu.add_widget(instance.bcbut)
        #instance.setmenu.add_widget(instance.hfbut)
        #instance.setmenu.add_widget(instance.conbut)
        instance.setmenu.add_widget(instance.rotbut)
        instance.setmenu.add_widget(instance.exitbut)   
        
    def bibutpress(instance, *kwargs):
        
        #remove main menu buttons from dropdown
        instance.setmenu.remove_widget(instance.bibut)
        instance.setmenu.remove_widget(instance.bcbut)
        #instance.setmenu.remove_widget(instance.hfbut)
        #instance.setmenu.remove_widget(instance.conbut)
        instance.setmenu.remove_widget(instance.rotbut)
        instance.setmenu.remove_widget(instance.exitbut)
        
        #create background image submenu buttons and assign each the function imgbutpress, passing in the source of each specific image
        instance.setmenu.dismiss
        imgbut0 = Button(text='Metal 1', size_hint_y= None, height= 30)
        imgbut0.bind(on_release=partial(instance.imgbutpress, 'Images/Metal.jpg'))
        imgbut1 = Button(text='Metal 2', size_hint_y= None, height= 30)
        imgbut1.bind(on_release=partial(instance.imgbutpress, 'Images/Metal2.jpg'))
        imgbut2 = Button(text='Blue', size_hint_y= None, height= 30)
        imgbut2.bind(on_release=partial(instance.imgbutpress, 'Images/bgcblue.jpg'))
        imgbut3 = Button(text='Black', size_hint_y= None, height= 30)
        imgbut3.bind(on_release=partial(instance.imgbutpress, 'Images/bgcblack.jpg'))
        imgbut4 = Button(text='Red', size_hint_y= None, height= 30)
        imgbut4.bind(on_release=partial(instance.imgbutpress, 'Images/bgcred.jpg'))
        imgbut5 = Button(text='Yellow', size_hint_y= None, height= 30)
        imgbut5.bind(on_release=partial(instance.imgbutpress, 'Images/bgcyellow.jpg'))
        imgbut6 = Button(text='Green', size_hint_y= None, height= 30)
        imgbut6.bind(on_release=partial(instance.imgbutpress, 'Images/bgcgreen.jpg'))
        imgbut7 = Button(text='White', size_hint_y= None, height= 30)
        imgbut7.bind(on_release=partial(instance.imgbutpress, 'Images/bgcwhite.jpg'))
        imgbut8 = Button(text='[Back]', size_hint_y= None, height= 30, color=(0, 1, 0, 1))
        imgbut8.bind(on_release=partial(instance.imgbutpress, 'none'))
        instance.imagebuttons = [imgbut0,imgbut1,imgbut2,imgbut3,imgbut4,imgbut5,imgbut6,imgbut7,imgbut8]
        
        #add background image submenu buttons
        instance.setmenu.add_widget(imgbut0)
        instance.setmenu.add_widget(imgbut1)
        instance.setmenu.add_widget(imgbut2)
        instance.setmenu.add_widget(imgbut3)
        instance.setmenu.add_widget(imgbut4)
        instance.setmenu.add_widget(imgbut5)
        instance.setmenu.add_widget(imgbut6)
        instance.setmenu.add_widget(imgbut7)
        instance.setmenu.add_widget(imgbut8)
        instance.setmenu.open
    
    def bcbutpress(instance, *largs):
        
        #remove main menu buttons from dropdown
        instance.setmenu.remove_widget(instance.bibut)
        instance.setmenu.remove_widget(instance.bcbut)
        #instance.setmenu.remove_widget(instance.hfbut)
        #instance.setmenu.remove_widget(instance.conbut)
        instance.setmenu.remove_widget(instance.rotbut)
        instance.setmenu.remove_widget(instance.exitbut)
        
        #add submenu buttons
        brightbut00 = Button(text='0%', size_hint_y= None, height= 30)
        brightbut00.bind(on_release=partial(instance.brightbutpress, '24'))
        brightbut0 = Button(text='25%', size_hint_y= None, height= 30)
        brightbut0.bind(on_release=partial(instance.brightbutpress, '64'))
        brightbut1 = Button(text='50%', size_hint_y= None, height= 30)
        brightbut1.bind(on_release=partial(instance.brightbutpress, '128'))
        brightbut2 = Button(text='75%', size_hint_y= None, height= 30)
        brightbut2.bind(on_release=partial(instance.brightbutpress, '196'))
        brightbut3 = Button(text='100%', size_hint_y= None, height= 30)
        brightbut3.bind(on_release=partial(instance.brightbutpress, '255'))
        brightbut4 = Button(text='[Back]', size_hint_y= None, height= 30, color=(0, 1, 0, 1))
        brightbut4.bind(on_release=partial(instance.brightbutpress, 'back'))
        
        instance.brightbuttons = [brightbut00,brightbut0,brightbut1,brightbut2,brightbut3,brightbut4]
        
        instance.setmenu.add_widget(brightbut00)
        instance.setmenu.add_widget(brightbut0)
        instance.setmenu.add_widget(brightbut1)
        instance.setmenu.add_widget(brightbut2)
        instance.setmenu.add_widget(brightbut3)
        instance.setmenu.add_widget(brightbut4)
        
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
        instance.Parent.save_settings()
        print('The button <%s> is being pressed' % instance.exitbut.text)
        App.get_running_app().stop()
    #sys.exit()
