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
        
        #GAUGE SPECIFIC VALUES
        self.Measure = 'DEFAULT'
        self.MinValue= 0
        self.MaxValue= 80
        self.Units= 'DEF'

        #BACKGROUND       
        self.gauge = Image(source='Images/Guages/GuageSquare.png', size=(400,400))
        
        """
        #SETTINGS MENU BUTTON
        self.settings= Button(text='Modify', pos=(155,40), size=(80,30), color=(51,102,255,1))
        self.settings.bind(on_release=self.menu)
        self.settings_open=False
        """
        #GUAGE VALUE
        self.VALUE = Label(text='0', font_size='40sp', pos=(30,30))
        
        
        #GUAGE MEASUREMENTS AND UNTIS
        self.MTitle = Label(text=self.Measure, font_size='26sp', pos=(150,40), color=(0, 0, 0, 1))
        self.MUnits = Label(text=self.Units, font_size='22sp', pos=(150,70), color=(0, 0, 0, 1))
        
        
        #ADDING TO WIDGET
        self.add_widget(self.gauge)
        
        self.add_widget(self.MTitle)
        self.add_widget(self.MUnits)
        self.add_widget(self.VALUE)


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

    
        


    
