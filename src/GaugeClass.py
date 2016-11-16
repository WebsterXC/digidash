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
from can import canbus, daemon


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
        self.PID = None #ADD THIS VALUE TO setGaugeParameters

        #BACKGROUND   
        self.gauge = Image(source='Images/Gauges/GaugeHead1.png', size=(400,400))
        self.style = 1
        
        #GAUGE DIAL
        self.dialscat = Scatter(do_translation=False)
        self.dialscat.center = self.gauge.center
        self.dial = Image(source='Images/dial.png',size=(300,300), pos=(-105,-90))
        self.dialscat.add_widget(self.dial)
        self.dialscat.rotation = 1
        #self.dialscat.bind(on_touchdown=self.TestRotation)
        
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
    ___________________________________________________________
    |                                                            |
    |                    MENU CREATION FUNCTIONS                    |
    |                                                            |
    |    THESE FUCNTIONS CREATE GAUGE CUSTOMIZATION MENUS         |
    |    MENUS INCLUDE:                                            |
    |        MAIN MENU (menu)                                    |
    |            -THEME MENU    (preset_themes_menu)                |
    |            -GAUGE BACKGROUND MENU (gauge_background_menu)    |
    |            -GAUGE DIAL MENU (gauge_dial_menu)                |
    |            -GAUGE RIM MENU
    |            _TEXT COLOR MENU
    |___________________________________________________________|
    """    
        
    def menu(self, *largs):
        if(self.settings_open==False):
            menu = BoxLayout(
                    size_hint=(0.25, (0.05*7)),
                    orientation='vertical')
            
            PST = Button(text='Preset Themes')
            PST.bind(on_release=self.preset_themes_menu)
            
            GBG = Button(text='Gauge Background')
            GBG.bind(on_release=self.gauge_background_menu)
            
            GDB = Button(text='Gauge Dial')
            GDB.bind(on_release=self.gauge_dial_menu)
            
            GRB = Button(text='Gauge Rim')
            GRB.bind(on_release=self.gauge_rim_menu)
            
            GTC = Button(text='Text Color')
            GTC.bind(on_release=self.gauge_text_menu)
            
            delete = Button(text='[ DELETE ]')
            delete.bind(on_release=self.deleteGauge)
            
            close = Button(text='[ CLOSE ]')
            close.bind(on_release=self.close_menus)
            
            menu.add_widget(PST)
            menu.add_widget(GBG)
            menu.add_widget(GDB)
            menu.add_widget(GTC)
            menu.add_widget(delete)
            menu.add_widget(close)
            
            menu.pos=self.Scat.pos
            self.gmenu=menu
            self.Parent.appLayout.add_widget(menu)
            self.settings_open=True
            self.settings.text='Close'
        else:
            self.close_menus()
            
    def preset_themes_menu(self,*largs):
        """
            Changes overall theme of gauge
        """
        theme_menu = BoxLayout(
                size_hint=(0.25, (0.05*9)),
                orientation='vertical')
            
        B1 = Button(text='Style 1')
        B1.bind(on_release=self.style_1)
        B2 = Button(text='Style 2')
        B2.bind(on_release=self.style_2)
        B3 = Button(text='Style 3')
        B3.bind(on_release=self.style_3)
        B4 = Button(text='Style 4')
        B4.bind(on_release=self.style_4)
        B5 = Button(text='Style 5')
        B5.bind(on_release=self.style_5)
        B6 = Button(text='Style 6')
        B6.bind(on_release=self.style_6)
        B7 = Button(text='Style 7')
        B7.bind(on_release=self.style_7)
        
        back = Button(text='[ BACK ]')
        back.bind(on_release=self.back_to_menu)
        close = Button(text='[ CLOSE ]')
        close.bind(on_release=self.close_menus)
            
        theme_menu.add_widget(back)
        theme_menu.add_widget(B1)
        theme_menu.add_widget(B2)
        theme_menu.add_widget(B3)
        theme_menu.add_widget(B4)
        theme_menu.add_widget(B5)
        theme_menu.add_widget(B6)
        theme_menu.add_widget(B7)
        theme_menu.add_widget(close)
        
        theme_menu.pos=self.Scat.pos
        
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.gmenu=theme_menu
        self.Parent.appLayout.add_widget(theme_menu)
        
    def gauge_background_menu(self, *largs):
        bg_menu = BoxLayout(
                    size_hint=(0.25, (0.05*9)),
                    orientation='vertical')
            
        BG1 = Button(text='WHITE')
        BG1.bind(on_release=self.bg_1)
        BG2 = Button(text='PURPLE')
        BG2.bind(on_release=self.bg_2)
        BG3 = Button(text='BLACK')
        BG3.bind(on_release=self.bg_3)
        BG4 = Button(text='YELLOW')
        BG4.bind(on_release=self.bg_4)
        BG5 = Button(text='BLUE')
        BG5.bind(on_release=self.bg_5)
        BG6 = Button(text='GREEN')
        BG6.bind(on_release=self.bg_6)
        BG7 = Button(text='RED')
        BG7.bind(on_release=self.bg_7)
        
        back = Button(text='[ BACK ]')
        back.bind(on_release=self.back_to_menu)
        close = Button(text='[ CLOSE ]')
        close.bind(on_release=self.close_menus)
        
        
        bg_menu.add_widget(BG1)
        bg_menu.add_widget(BG2)
        bg_menu.add_widget(BG3)
        bg_menu.add_widget(BG4)
        bg_menu.add_widget(BG5)
        bg_menu.add_widget(BG6)
        bg_menu.add_widget(BG7)
        bg_menu.add_widget(close)
        
        bg_menu.pos=self.Scat.pos
        
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.gmenu=bg_menu
        self.Parent.appLayout.add_widget(bg_menu)
    
    def gauge_dial_menu(self, *largs):
        dial_menu = BoxLayout(
                    size_hint=(.25, (0.05*9)),
                    orientation='vertical')
            
        BD1 = Button(text='WHITE')
        BD1.bind(on_release=self.dial_1)
        BD2 = Button(text='PURPLE')
        BD2.bind(on_release=self.dial_2)
        BD3 = Button(text='BLACK')
        BD3.bind(on_release=self.dial_3)
        BD4 = Button(text='YELLOW')
        BD4.bind(on_release=self.dial_4)
        BD5 = Button(text='BLUE')
        BD5.bind(on_release=self.dial_5)
        BD6 = Button(text='GREEN')
        BD6.bind(on_release=self.dial_6)
        BD7 = Button(text='RED')
        BD7.bind(on_release=self.dial_7)
        
        back = Button(text='[ BACK ]')
        back.bind(on_release=self.back_to_menu)
        close = Button(text='[ CLOSE ]')
        close.bind(on_release=self.close_menus)
        
        dial_menu.add_widget(back)
        dial_menu.add_widget(BD1)
        dial_menu.add_widget(BD2)
        dial_menu.add_widget(BD3)
        dial_menu.add_widget(BD4)
        dial_menu.add_widget(BD5)
        dial_menu.add_widget(BD6)
        dial_menu.add_widget(BD7)
        dial_menu.add_widget(close)
        
        dial_menu.pos=self.Scat.pos
        
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.gmenu=dial_menu
        self.Parent.appLayout.add_widget(dial_menu)
    
    def gauge_rim_menu(self, *largs):
        """
        GAUGE RIM
                -SILVER
                -STEEL
                -GOLD
                -BRONZE
                -BLACK
        """
        rim_menu = BoxLayout(
                    size_hint=(0.25, (0.05*7)),
                    orientation='vertical')
            
        GD1 = Button(text='SILVER')
        GD1.bind(on_release=self.dial_1)
        GD2 = Button(text='STEEL')
        GD2.bind(on_release=self.dial_2)
        GD3 = Button(text='GOLD')
        GD3.bind(on_release=self.dial_3)
        GD4 = Button(text='BRONZE')
        GD4.bind(on_release=self.dial_4)
        GD5 = Button(text='BLACK')
        GD5.bind(on_release=self.dial_5)

        back = Button(text='[ BACK ]')
        back.bind(on_release=self.back_to_menu)
        close = Button(text='[ CLOSE ]')
        close.bind(on_release=self.close_menus)

        rim_menu.add_widget(back)
        rim_menu.add_widget(GD1)
        rim_menu.add_widget(GD2)
        rim_menu.add_widget(GD3)
        rim_menu.add_widget(GD4)
        rim_menu.add_widget(GD5)
        rim_menu.add_widget(close)
        
        rim_menu.pos = self.Scat.pos
        
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.gmenu = rim_menu
        self.Parent.appLayout.add_widget(dial_menu)
        
        gauge_text_menu
    
    def gauge_text_menu(self, *largs):
        """
        """
        text_menu = BoxLayout(
                    size_hint=(0.25, (0.05*4)),
                    orientation='vertical')
            
        GT1 = Button(text='BLACK')
        GT1.bind(on_release=self.black_font)
        GT2 = Button(text='WHITE')
        GT2.bind(on_release=self.white_font)

        back = Button(text='[ BACK ]')
        back.bind(on_release=self.back_to_menu)
        close = Button(text='[ CLOSE ]')
        close.bind(on_release=self.close_menus)
            
        text_menu.add_widget(back)    
        text_menu.add_widget(GT1)
        text_menu.add_widget(GT2)
        text_menu.add_widget(close)
        
        text_menu.pos = self.Scat.pos
        
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.gmenu = text_menu
        self.Parent.appLayout.add_widget(text_menu)

    
    """
     ___________________________________________________________
    |                                                            |
    |                    GAUGE UTILITY FUNCTIONS                    |
    |                                                            |
    |___________________________________________________________
    """    
    
    def setVALUE(self, *largs):
        #MIN ANGLE: 360
        #MAX ANGLE: 88
        #ANGLE RANGE: 272    
        val_range = self.MaxValue-self.MinValue
        scale = 272.0/val_range
        
        #SHOULD BE:
        #val = canbus.CANdata[self.PID]
        #FOR TESTING USE:
        val = canbus.CANdata[0x0C]
        angle = 360 - (scale*val)
        #print('Range:' + str(val_range) + '  Scale:' + str(scale) + '  Value:' + str(val) + '  Angle:'+ str(angle))
        self.dialscat.rotation=angle
    
    
    def setParents(self, P, S):
        self.Parent=P
        self.Scat=S     
    
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

    def back_to_menu(self, *largs):
        self.close_menus()
        self.menu()

        
    def close_menus(self, *largs):
        """
            Closes open menu
        """
        self.Parent.appLayout.remove_widget(self.gmenu)
        self.settings_open=False
        self.settings.text='Modify'
        

    def setBackground(self, imagesrc, *largs):
        #Helper fuction to modify gauges background image
        self.gauge.source = imagesrc
        
    def deleteGauge(self, *largs):
        #Gauges are stored in the scatter in the main class in both the active gauge list 
        #and the appLayout visually. Remove from both to delete current gauge
        #self.Parent.ActiveGauges.remove(self.Scat)
        self.Parent.appLayout.remove_widget(self.Scat)
    
    
        
    """
     ___________________________________________________________
    |                                                            |
    |                    THEME FUNCTIONS                            |
    |                                                            |
    |    THEME DEFINES BACKGROUND, DIAL, FONT COLOR, AND RIM        |
    |                                                            |
    |___________________________________________________________|
    """    
        
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
        
    """
     ___________________________________________________________
    |                                                            |
    |                    BACKGROUND FUNCTIONS                    |
    |                                                            |
    |    THESE FUNCTIONS ONLY CHANGE BACKGROUND IMAGES SOURCE    |
    |                                                            |
    |___________________________________________________________|
    """    
        
    def bg_1(self, *largs):
        # Gauge Background Image [WHITE]
        self.setBackground('Images/Gauges/GaugeHead1.png')
    
    def bg_2(self, *largs):
        # Gauge Background Image []
        self.setBackground('Images/Gauges/GaugeHead2.png')
    
    def bg_3(self, *largs):
        self.setBackground('Images/Gauges/GaugeHead3.png')
    
    def bg_4(self, *largs):
        self.setBackground('Images/Gauges/GaugeHead4.png')
    
    def bg_5(self, *largs):
        self.setBackground('Images/Gauges/GaugeHead5.png')
        
    def bg_6(self, *largs):
        self.setBackground('Images/Gauges/GaugeHead6.png')
        
    def bg_7(self, *largs):
        self.setBackground('Images/Gauges/GaugeHead7.png')
        
    """
     ___________________________________________________________
    |                                                            |
    |                    DIAL FUNCTIONS                            |
    |                                                            |
    |        THESE FUNCTIONS ONLY CHANGE DIAL IMAGE SOURCES        |
    |                                                            |
    |___________________________________________________________|
    """    
        
    def dial_1(self, *largs):
        self.dial.source='Images/dial.png'
        
    def dial_2(self, *largs):
        self.dial.source='Images/dial.png'
    
    def dial_3(self, *largs):
        self.dial.source='Images/dial.png'
    
    def dial_4(self, *largs):
        self.dial.source='Images/dial.png'
        
    def dial_5(self, *largs):
        self.dial.source='Images/dial.png'
        
    def dial_6(self, *largs):
        self.dial.source='Images/dial.png'
    
    def dial_7(self, *largs):
        self.dial.source='Images/dial.png'

    
    """
    ___________________________________________________________
    |                                                            |
    |                    RIM FUNCTIONS                            |
    |                                                            |
    |        THESE FUNCTIONS ONLY CHANGE RIM IMAGE SOURCES        |
    |                                                            |
    |___________________________________________________________|
    """    
        
    def rim_1(self, *largs):
        #self.dial.source='Images/dial.png'
        print('ADD RIM IMAGES')
        
    def rim_2(self, *largs):
        print('ADD RIM IMAGES')
    
    def rim_3(self, *largs):
        print('ADD RIM IMAGES')
    
    def rim_4(self, *largs):
        print('ADD RIM IMAGES')
        
    def rim_5(self, *largs):
        print('ADD RIM IMAGES')
        
        
        
    """
    ___________________________________________________________
    |                                                            |
    |                    TEXT FUNCTIONS                            |
    |                                                            |
    |       THESE FUNCTIONS ONLY CHANGE FONT COLOR OF GAUGES        |
    |                                                            |
    |___________________________________________________________|
    """    
        
    def black_font(self, *largs):
        for l in self.UnitScaleLabels:
            l.color=(0,0,0,1)
        #String Identifiers
        self.MTitle.color=(0,0,0,1)
        self.MUnits.color=(0,0,0,1)
        
    def white_font(self, *largs):
        for l in self.UnitScaleLabels:
            l.color=(1,1,1,1)
        #String Identifiers
        self.MTitle.color=(1,1,1,1)
        self.MUnits.color=(1,1,1,1)
    
    
