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
from operator import pos



class GaugeDigital(Widget):
    def __init__(self, **kwargs):
        super(GaugeDigital, self).__init__(**kwargs)
        
        #REF TO MAIN CLASS
        self.Parent = None
        self.Scat = None;
        
        #GAUGE SPECIFIC VALUES
        self.Measure = 'DEFAULT'
        self.MinValue= 0
        self.MaxValue= 80
        self.Units= 'DEF'

        #BACKGROUND       
        self.gauge = Image(source='Images/Guages/GuageSquare1.png', size=(400,400))
        
        """
        #SETTINGS MENU BUTTON
        self.settings= Button(text='Modify', pos=(155,40), size=(80,30), color=(51,102,255,1))
        self.settings.bind(on_release=self.menu)
        self.settings_open=False
        """
        #GUAGE VALUE
        self.VALUE = Label(text='0', font_size='120sp', pos=(150,160), color=(0, 0, 0, 1))
        
        #SETTINGS MENU BUTTON
        self.settings= Button(text='Modify', pos=(155,40), size=(80,30), color=(51,102,255,1))
        self.settings.bind(on_release=self.menu)
        self.settings_open=False
        
        #GUAGE MEASUREMENTS AND UNTIS
        self.MTitle = Label(text=self.Measure, font_size='26sp', pos=(150,40), color=(0, 0, 0, 1))
        self.MUnits = Label(text=self.Units, font_size='22sp', pos=(150,70), color=(0, 0, 0, 1))
        
        
        #ADDING TO WIDGET
        self.add_widget(self.gauge)
        self.add_widget(self.settings)
        self.add_widget(self.MTitle)
        self.add_widget(self.MUnits)
        self.add_widget(self.VALUE)
        
    def setParents(self, P, S):
        self.Parent=P
        self.Scat=S 


    def setBackground(self, imagesrc, *largs):
        self.gauge.source = imagesrc
        
        
    def setGuageParameters(self, Meas, Min, Max, UnitM):
        self.Measure= Meas
        #UPDATE TEXT
        self.MTitle.text=Meas
        
        self.Units= UnitM
        self.MUnits.text=UnitM
        
        

    def setVALUE(self, val):
        self.VALUE.text= val

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

    def style_1(self, *largs):
        self.setBackground('Images/Guages/GuageSquare1.png')
        
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
        self.VALUE.color=(0,0,0,1)
    
    def style_2(self, *largs):
        self.setBackground('Images/Guages/GuageSquare2.png')
        
        self.MTitle.color=(255,255,255,1)
        self.MUnits.color=(255,255,255,1)
        self.VALUE.color=(255,255,255,1)
        
        
    def style_3(self, *largs):
        self.setBackground('Images/Guages/GuageSquare3.png')
        
        self.MTitle.color=(255,255,255,1)
        self.MUnits.color=(255,255,255,1)
        self.VALUE.color=(255,255,255,1)
    