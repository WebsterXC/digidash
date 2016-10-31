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



class Gauge(Widget):
    def __init__(self, **kwargs):
        super(Gauge, self).__init__(**kwargs)
        
        #REF TO MAIN CLASS
        self.Parent = None
        self.Scat = None;
        
        #GAUGE SPECIFIC VALUES
        self.Measure = 'DEFAULT'
        self.MinValue= 0
        self.MaxValue= 80
        self.Units= 'DEF'

        #BACKGROUND       
        self.gauge = Image(source='Images/Guages/GuageHead5.png', size=(400,400))
        
        #GAUGE DIAL
        self.dialscat = Scatter(do_translation=False)
        self.dialscat.center = self.gauge.center
        self.dial = Image(source='Images/dial.png',size=(300,300), pos=(-105,-90))
        self.dialscat.add_widget(self.dial)
        self.dialscat.rotation = 1
        self.dialscat.bind(on_touchdown=self.TestRotation)
        
        #VALUE INCRIMENT LABELS
        self.L1 =Label(text='0', font_size='20sp', pos=(70,70), color=(0, 0, 0, 1))
        self.L2 =Label(text='10', font_size='20sp', pos=(30,125), color=(0, 0, 0, 1))
        self.L3 =Label(text='20', font_size='20sp', pos=(40,195), color=(0, 0, 0, 1))
        self.L4 =Label(text='30', font_size='20sp', pos=(80,255), color=(0, 0, 0, 1))
        self.L5 =Label(text='40', font_size='20sp', pos=(145,280), color=(0, 0, 0, 1))
        self.L6 =Label(text='50', font_size='20sp', pos=(220,265), color=(0, 0, 0, 1))
        self.L7 =Label(text='60', font_size='20sp', pos=(260,205), color=(0, 0, 0, 1))
        self.L8 =Label(text='70', font_size='20sp', pos=(280,125), color=(0, 0, 0, 1))
        self.L9 =Label(text='80', font_size='20sp', pos=(240,65), color=(0, 0, 0, 1))
        
        #SETTINGS MENU BUTTON
        self.settings= Button(text='Modify', pos=(155,40), size=(80,30), color=(51,102,255,1))
        self.settings.bind(on_release=self.menu)
        self.settings_open=False
        
        #GUAGE MEASUREMENTS AND UNTIS
        self.MTitle = Label(text=self.Measure, font_size='26sp', pos=(150,40), color=(0, 0, 0, 1))
        self.MUnits = Label(text=self.Units, font_size='22sp', pos=(150,70), color=(0, 0, 0, 1))
        
        
        #ADDING TO WIDGET
        self.add_widget(self.gauge)
        self.add_widget(self.dialscat)
        self.add_widget(self.settings)
        
        self.add_widget(self.MTitle)
        self.add_widget(self.MUnits)
        
        self.add_widget(self.L1)
        self.add_widget(self.L2)
        self.add_widget(self.L3)
        self.add_widget(self.L4)
        self.add_widget(self.L5)
        self.add_widget(self.L6)
        self.add_widget(self.L7)
        self.add_widget(self.L8)
        self.add_widget(self.L9)
        
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
                    size_hint=(None, None),
                    orientation='vertical')
            
            B1= Button(text='Style 1')
            B1.bind(on_release=self.style_1)
            B2= Button(text='Style 2')
            B2.bind(on_release=self.style_2)
            B3= Button(text='Style 3')
            B3.bind(on_release=self.style_3)
            
            menu.add_widget(B1)
            menu.add_widget(B2)
            menu.add_widget(B3)
            
            close = Button(text='close')
            close.bind(on_release=partial(self.close_menu, menu))
            menu.add_widget(close)
            menu.pos=self.Scat.pos
            self.Parent.appLayout.add_widget(menu)
            self.settings_open=True

    def close_menu(self, widget, *largs):
        """
            Closes open menu
        """
        self.Parent.appLayout.remove_widget(widget)
        self.settings_open=False

    def setBackground(self, imagesrc, *largs):
        self.gauge.source = imagesrc
        
    def style_1(self, *largs):
        self.setBackground('Images/Guages/GuageHead5.png')
        self.L1.color=(0,0,0,1)
        self.L2.color=(0,0,0,1)
        self.L3.color=(0,0,0,1)
        self.L4.color=(0,0,0,1)
        self.L5.color=(0,0,0,1)
        self.L6.color=(0,0,0,1)
        self.L7.color=(0,0,0,1)
        self.L8.color=(0,0,0,1)
        self.L9.color=(0,0,0,1)
        
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
    
    def style_2(self, *largs):
        self.setBackground('Images/Guages/GuageHead6.png')
        self.L1.color=(255,255,255,1)
        self.L2.color=(255,255,255,1)
        self.L3.color=(255,255,255,1)
        self.L4.color=(255,255,255,1)
        self.L5.color=(255,255,255,1)
        self.L6.color=(255,255,255,1)
        self.L7.color=(255,255,255,1)
        self.L8.color=(255,255,255,1)
        self.L9.color=(255,255,255,1)
        
        self.MTitle.color=(255,255,255,1)
        self.MUnits.color=(255,255,255,1)
        
        
    def style_3(self, *largs):
        self.setBackground('Images/Guages/GuageHead2.png')
        self.L1.color=(255,255,255,1)
        self.L2.color=(255,255,255,1)
        self.L3.color=(255,255,255,1)
        self.L4.color=(255,255,255,1)
        self.L5.color=(255,255,255,1)
        self.L6.color=(255,255,255,1)
        self.L7.color=(255,255,255,1)
        self.L8.color=(255,255,255,1)
        self.L9.color=(255,255,255,1)
        
        self.MTitle.color=(255,255,255,1)
        self.MUnits.color=(255,255,255,1)
        
    def setGuageParameters(self, Meas, Min, Max, UnitM):
        self.Measure= Meas
        #UPDATE TEXT
        self.MTitle.text=Meas
        
        self.Units= UnitM
        self.MUnits.text=UnitM
        
        self.MinValue=Min
        self.MaxValue=Max
        diff = Max-Min
        inc = diff/8
        self.L1.text=str(Min)
        self.L2.text=str(Min+(1*inc))
        self.L3.text=str(Min+(2*inc))
        self.L4.text=str(Min+(3*inc))
        self.L5.text=str(Min+(4*inc))
        self.L6.text=str(Min+(5*inc))
        self.L7.text=str(Min+(6*inc))
        self.L8.text=str(Min+(7*inc))
        self.L9.text=str(Min+(8*inc))
        

    def setMPH(self, mph):
        angle = 360-(1.3655*mph)
        self.dialscat.rotation=angle
        
    def MPH2Angle(self, mph):
        return (1.3655*mph)
       
    def TestRotation(self, *largs):
        angle = Gauge.MPH2Angle(self,80)
        anim = Animation(rotation=-angle, duration=6.)
        anim.start(self.dialscat)
    
        


    
