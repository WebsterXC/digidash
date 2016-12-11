#################################################
#   ======    =====    ======   =====
#   ||	 \\     |     //	  |
#   ||    \\    |    // 	  |
#   ||    //    |    ||  =====	  |   --------
#   ||   //     |    \\     //	  |
#   ======    =====   ======    =====
##################################################

# [Summary]:

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
from can import pids
from can import canbus 
import time, logging
import platform
import ConfigParser

gaugeName = " "

class AddGauge(Widget):
    log = None
    def __init__(self, **kwargs):
        super(AddGauge, self).__init__(**kwargs)
	
	self.log = logging.getLogger('digilogger')

        win_w = Window.size[0]
        win_h = Window.size[1]
        if(platform.platform()=='Linux-4.1.19-v7+-armv7l-with-Ubuntu-16.04-xenial'):
            win_h= 480

        self.Parent = None        
        self.dButton = None
        self.aButton = None

        self.appLayout = FloatLayout(size=(800,600))

        reads = read()
        self.typeDict = read.readIn(reads, "AddGauge.csv")

        self.codetype = DropDown()
       
        for x in self.typeDict.keys():
                
                #self.digi = Button(text='Digital Gauge', size_hint_y = None, height = 25)
                #self.digi.bind(on_release = partial(self.userSelect, x, 'digital'))
                #self.rage.add_widget(self.digi)
            
                #self.analo = Button(text='Analog Gauge', size_hint_y = None, height = 25)
                #self.analo.bind(on_release = partial(self.userSelect, x, 'analog'))
                #self.rage.add_widget(self.analo)
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
        win_h = Window.size[1]

        if (instance.dButton != None):
            instance.Parent.appLayout.remove_widget(instance.dButton)
            instance.dButton = None

        digi = Button(text='Digital Gauge', size_hint = (None, None), size = (150,30))
        digi.pos=(250,win_h-digi.size[1])
        digi.bind(on_release = partial(instance.makeGauge, val, 'digital'))
        instance.dButton = digi
        instance.Parent.appLayout.add_widget(digi)
          
        if (instance.aButton != None):
            instance.Parent.appLayout.remove_widget(instance.aButton)
            instance.aButton = None

        analo = Button(text='Analog Gauge', size_hint = (None, None), size = (150,30))
        analo.pos=(400,win_h-analo.size[1])
        analo.bind(on_release = partial(instance.makeGauge, val, 'analog'))
        instance.aButton = analo
        instance.Parent.appLayout.add_widget(analo)

    def makeGauge(instance, val, diana, *largs):
        instance.Parent.appLayout.remove_widget(instance.aButton)
        instance.aButton = None
        instance.Parent.appLayout.remove_widget(instance.dButton)
        instance.dButton = None
        if (diana == 'digital'):
            
            gstyle = 1
            gposx = 300
            gposy = 250
            gscale = 0.35
            gmeasure = instance.typeDict.get(val)[0]
            gunits = instance.typeDict.get(val)[3]
            gmin = float(instance.typeDict.get(val)[1])
            gmax = float(instance.typeDict.get(val)[2])
            gcode = str(instance.typeDict.get(val)[4])
            canbus.subscribe(gcode)

            newG = GaugeDigital()
            newG.PID = gcode
            newGS = Scatter(scale=gscale, scale_min=0.25, scale_max=1.5, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
            newGS.add_widget(newG)
            GaugeDigital.setParents(newG,instance.Parent,newGS)
            GaugeDigital.setGaugeParameters(newG, gmeasure, gmin, gmax, gunits)
            instance.Parent.ActiveGauges.append(newGS)
            instance.Parent.appLayout.add_widget(newGS)
                            
            Clock.schedule_interval(partial(GaugeDigital.setVALUE, newG), 0.005)

        else:
            gstyle = 1
            gposx = 330
            gposy = 220
            gscale = 0.35
            gmeasure = instance.typeDict.get(val)[0]
            gunits = instance.typeDict.get(val)[3]
            gmin = float(instance.typeDict.get(val)[1])
            gmax = float(instance.typeDict.get(val)[2])
            gcode = str(instance.typeDict.get(val)[4])
            canbus.subscribe(gcode)

            newG = Gauge()
            newG.PID = gcode
            newGS = Scatter(scale=gscale, scale_min=0.25, scale_max=1.5, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
            newGS.add_widget(newG)
            Gauge.setParents(newG,instance.Parent,newGS)
            Gauge.setGaugeParameters(newG, gmeasure, gmin, gmax, gunits)
            instance.Parent.ActiveGauges.append(newGS)
            instance.Parent.appLayout.add_widget(newGS)
                            
            Clock.schedule_interval(partial(Gauge.setVALUE, newG), 0.005)

