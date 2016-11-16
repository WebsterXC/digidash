from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from functools import partial
import time
from kivy.uix import floatlayout
from kivy.uix.behaviors import ButtonBehavior

from can import canbus, daemon, pids

class Gauge(Widget):
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        
        #REF TO MAIN CLASS
        self.Parent = None
        self.Scat = None
        
        #GAUGE SPECIFIC VALUES
        self.Measure = 'DEFAULT'
        self.MinValue= 0
        self.MaxValue= 80
        self.Units= 'DEF'
        self.PID = None #ADD THIS VALUE TO setGuageParameters
        
        #BACKGROUND   
        self.gauge = Image(source='Images/Gauges/GaugeHead1.png', size=(400,400))
        self.style = 1
        
        #GAUGE DIAL
        self.dialscat = Scatter(do_translation=False)
        self.dialscat.center = self.gauge.center
        self.dial = Image(source='Images/dial.png',size=(300,300), pos=(-105,-90))
        self.dialscat.add_widget(self.dial)
        self.dialscat.rotation = 1
        self.dialscat.bind(on_touchdown=self.TestRotation)
        
        #VALUE INCREMENT LABELS
        self.L1 =Label(text='0', font_size='20sp', pos=(70,70), color=(0, 0, 0, 1))
        self.L2 =Label(text='10', font_size='20sp', pos=(30,125), color=(0, 0, 0, 1))
        self.L3 =Label(text='20', font_size='20sp', pos=(40,195), color=(0, 0, 0, 1))
        self.L4 =Label(text='30', font_size='20sp', pos=(80,255), color=(0, 0, 0, 1))
        self.L5 =Label(text='40', font_size='20sp', pos=(145,280), color=(0, 0, 0, 1))
        self.L6 =Label(text='50', font_size='20sp', pos=(220,265), color=(0, 0, 0, 1))
        self.L7 =Label(text='60', font_size='20sp', pos=(260,205), color=(0, 0, 0, 1))
        self.L8 =Label(text='70', font_size='20sp', pos=(280,125), color=(0, 0, 0, 1))
        self.L9 =Label(text='80', font_size='20sp', pos=(240,65), color=(0, 0, 0, 1))
        
        self.UnitScaleLabels = [self.L1,self.L2,self.L3,self.L4,self.L5,self.L6,self.L7,self.L8,self.L9]
        
        #SETTINGS MENU BUTTON
        self.settings= Button(text='Modify', pos=(155,40), size=(80,30), color=(51,102,255,1))
        self.settings.bind(on_release=self.menu)
        self.settings_open=False
        #REF TO MENU
        self.gmenu= None
        
        #GAUGE MEASUREMENTS AND UNTIS
        self.MTitle = Label(text=self.Measure, font_size='26sp', pos=(150,40), color=(0, 0, 0, 1))
        self.MUnits = Label(text=self.Units, font_size='22sp', pos=(150,70), color=(0, 0, 0, 1))
        
        
        #ADDING TO WIDGET
        self.add_widget(self.gauge)
        self.add_widget(self.dialscat)
        self.add_widget(self.settings)
        
        self.add_widget(self.MTitle)
        self.add_widget(self.MUnits)
        
        #ADD UNIT SCALE LABELS
        for l in self.UnitScaleLabels:
            self.add_widget(l)
        """
        self.add_widget(self.L1)
        self.add_widget(self.L2)
        self.add_widget(self.L3)
        self.add_widget(self.L4)
        self.add_widget(self.L5)
        self.add_widget(self.L6)
        self.add_widget(self.L7)
        self.add_widget(self.L8)
        self.add_widget(self.L9)
        """
        
    def setParents(self, P, S):
        self.Parent=P
        self.Scat=S        
    
    def changeBGTest(self):
        self.Parent.bg.source='Images/Metal.jpg'  
        
    def menu(self, *largs):
        """
            Creates a menu to modify Gauge style
        """
        if(self.settings_open==False):
            menu = BoxLayout(
                    size_hint=(None, .5),
                    orientation='vertical')
            
            B1= Button(text='Style 1')
            B1.bind(on_release=self.style_1)
            B2= Button(text='Style 2')
            B2.bind(on_release=self.style_2)
            B3= Button(text='Style 3')
            B3.bind(on_release=self.style_3)
            B4= Button(text='Style 4')
            B4.bind(on_release=self.style_4)
            B5= Button(text='Style 5')
            B5.bind(on_release=self.style_5)
            B6= Button(text='Style 6')
            B6.bind(on_release=self.style_6)
            B7= Button(text='Style 7')
            B7.bind(on_release=self.style_7)
            
            menu.add_widget(B1)
            menu.add_widget(B2)
            menu.add_widget(B3)
            menu.add_widget(B4)
            menu.add_widget(B5)
            menu.add_widget(B6)
            menu.add_widget(B7)
            
            
            close = Button(text='close')
            close.bind(on_release=partial(self.close_menu, menu))
            menu.add_widget(close)
            menu.pos=self.Scat.pos
            self.gmenu=menu
            self.Parent.appLayout.add_widget(menu)
            self.settings_open=True
            self.settings.text='Close'
        else:
            self.close_menu(self.gmenu)


    def close_menu(self, widget, *largs):
        """
            Closes open menu
        """
        self.Parent.appLayout.remove_widget(widget)
        self.settings_open=False
        self.settings.text='Modify'

    def setBackground(self, imagesrc, *largs):
        self.gauge.source = imagesrc
        
    def style_1(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead1.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(0,0,0,1)
        
        #String Identifiers
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
    
    def style_2(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead2.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(1,1,1,1)
        
        #String Identifiers
        self.MTitle.color=(1,1,1,1)
        self.MUnits.color=(1,1,1,1)
        
        
    def style_3(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead3.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(1,1,1,1)
        
        #String Identifiers
        self.MTitle.color=(1,1,1,1)
        self.MUnits.color=(1,1,1,1)
        
    def style_4(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead4.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(1,0,0,1)
        
        #String Identifiers
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
    
    def style_5(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead5.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(1,1,1,1)
        
        #String Identifiers
        self.MTitle.color=(1,1,1,1)
        self.MUnits.color=(1,1,1,1)
        
    def style_6(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead6.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(0,0,0,1)
        
        #String Identifiers
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
    
    def style_7(self, *largs):
        #Theme Background Image
        self.setBackground('Images/Gauges/GaugeHead7.png')
        
        #Unit Measure Colors
        for l in self.UnitScaleLabels:
            l.color=(1,1,1,1)
        
        #String Identifiers
        self.MTitle.color=(1,1,1,1)
        self.MUnits.color=(1,1,1,1)
        
    def setGaugeParameters(self, Meas, Min, Max, UnitM):
        #ADD PID VALUE
        self.Measure= Meas
        #UPDATE TEXT
        self.MTitle.text=Meas
        
        self.Units= UnitM
        self.MUnits.text=UnitM
        
        self.MinValue=Min
        self.MaxValue=Max
        diff = Max-Min
        inc = diff/8
        
        #Set unit scale text values
        for n in range(9):
            self.UnitScaleLabels[n].text=str(Min+(n*inc))
    
    def setVALUE(self, *largs):
        #MIN ANGLE: 360
        #MAX ANGLE: 88
        #ANGLE RANGE: 272
	
        val_range = self.MaxValue-self.MinValue
        scale = 272.0/val_range
        
        #SHOULD BE:
	val = canbus.CANdata[self.PID]
        angle = 360 - (scale*val)
	#print('Range:' + str(val_range) + '  Scale:' + str(scale) + '  Value:' + str(val) + '  Angle:'+ str(angle))
        self.dialscat.rotation=angle
	
	#self.dialscat.rotation=88

    def setMPH(self, mph):
        angle = 360-(1.3655*mph)
        self.dialscat.rotation=angle
        
    def MPH2Angle(self, mph):
        return (1.3655*mph)
       
    def TestRotation(self, *largs):
        angle = Gauge.MPH2Angle(self,80)
        anim = Animation(rotation=-angle, duration=6.)
	anim.start(self.dialscat)
