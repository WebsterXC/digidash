from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.clock import Clock
from functools import partial
from readIn import read
from GaugeClass import Gauge
from GaugeClassDigital import GaugeDigital 
import time
import platform
import ConfigParser


class AddGauge(Widget):
    #global typeDict

    def __init__(self, **kwargs):
        super(AddGauge, self).__init__(**kwargs)

        win_w = Window.size[0]
        win_h = Window.size[1]
        if(platform.platform()=='Linux-4.1.19-v7+-armv7l-with-Ubuntu-16.04-xenial'):
            win_h= 480

        #REF TO PARENT CLASS
        self.Parent = None

        self.appLayout = FloatLayout(size=(800,600))

        reads = read()
        self.typeDict = read.readIn(reads,"AddGauge.csv")
        #print type

        #self.Values= ['Engine Load',
         #        'Fuel Pressure',
          #       'Tachometer',
           #     'Speedometer',
            #    'MAF',
             #   'Throttle Pos',
              #  'Boost Pressure']


        self.codetype = DropDown()

        for x in self.typeDict.keys():
            self.cur = Button(text=x, size_hint_y= None, height= 30)
            self.cur.bind(on_release = partial(self.userSelect, x))  
            self.codetype.add_widget(self.cur)

        self.mainbutton = Button(text='New Gauge', size_hint=(None,None), size=(200,30))
        self.mainbutton.pos=(20,win_h-self.mainbutton.size[1])
        self.mainbutton.bind(on_release=self.codetype.open)
        self.add_widget(self.mainbutton)

    def __resize__(instance):
        instance.mainbutton.pos=(20,win_h-self.mainbutton.size[1])

    def set_parent(self,p):
        self.Parent = p

    def userSelect(instance, val, *largs):
        
        #print(val)
        gtype = 'digital' #WHAT DO WE DO HERE?
        #print(gtype)
        gstyle = 1
        gposx = 50
        gposy = 150
        gscale = 0.35
        gmeasure = instance.typeDict.get(val)[0]
        print(gmeasure)
        gunits = instance.typeDict.get(val)[3]
        print(gunits)
        gmin = float(instance.typeDict.get(val)[1])
        print(gmin)
        gmax = float(instance.typeDict.get(val)[2])
        print(gmax)
       
        newG = GaugeDigital()
        newGS = Scatter(scale=gscale, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
        newGS.add_widget(newG)
        GaugeDigital.setParents(newG,instance.Parent,newGS)
        GaugeDigital.setGaugeParameters(newG, gmeasure, gmin, gmax, gunits)
        #Parent.ActiveGauges.append(newGS)
        #self.Parent.appLayout.add_widget(newGS)
                        
        Clock.schedule_interval(partial(GaugeDigital.setVALUE, newG), 0.0625)
