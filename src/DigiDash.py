from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.uix.scatterlayout import ScatterLayout
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from GaugeClass import Gauge  Gauge.setParents(g1,self,g1s)
from GaugeClassDigital import GaugeDigital
from Settings import Settings
from AddGauge import AddGauge
from Header import Header
from Footer import Footer
from kivy.uix.dropdown import DropDown
import time
from functools import partial
import ConfigParser


class DigiDashApp(App):
    def build(self):
        
        Config = ConfigParser.ConfigParser()
        Config.read("Settings.ini")
        GaugeList= Config.sections()[1:]
        
        ActiveGauges=[]
        
        for g in GaugeList:
            gtype = Config.get(g,'type')
            gstyle = int(Config.get(g,'style'))
            gposx = int(Config.get(g,'posx'))
            gposy = int(Config.get(g,'posy'))
            gscale = float(Config.get(g,'scale'))
            gmeasure = Config.get(g,'measure')
            gunits = Config.get(g,'units')
            gmin = int(Config.get(g,'min'))
            gmax = int(Config.get(g,'max'))
            
            print(g)
            print(gtype,gstyle,gposx,gposy,gscale,gmeasure,gunits,gmin,gmax)
            
            
            if(gtype == 'analog'):
                curG = Gauge()
                curGS = Scatter(scale=gscale, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                Gauge.setParents(curG,self,curGS)
                Gauge.setGuageParameters(curG, gmeasure, gmin, gmax, gunits)
                ActiveGauges.append(curGS)
            
            else:
                curG = GaugeDigital()
                curGS = Scatter(scale=gscale, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                GaugeDigital.setParents(curG,self,curGS)
                GaugeDigital.setGuageParameters(curG, gmeasure, gmin, gmax, gunits)
                ActiveGauges.append(curGS)
            
            
        #print(GaugeList)
        
        #Define application layout
        self.appLayout = FloatLayout(size=(800,600))

        #Create initial background, replace eventually with settings load from ini file
        self.bg = Image(source='Images/Metal2.jpg', pos=(0,0), size=(1500,840))
        
        """
        #Create all initial guages, switch eventually to load from settings ini file
        g1= Gauge()
        g1s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(30,80))
        g1s.add_widget(g1)
        Gauge.setParents(g1,self,g1s)
        #Gauge.changeBGTest(g1)
        Gauge.setGuageParameters(g1, 'Speedometer', 0, 80, 'MPH')
        #Gauge.setBackground(g1,'Images/Guages/GuageHead3.png')
        
        g2= Gauge()
        g2s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(220,80))
        g2s.add_widget(g2)
        Gauge.setParents(g2,self,g2s)
        Gauge.setGuageParameters(g2, 'Fuel Pressure', 0, 80, 'PSI')
        g2.setMPH(100)

        g3= Gauge()
        g3s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(420,80))
        g3s.add_widget(g3)
        Gauge.setParents(g3,self,g3s)
        Gauge.setGuageParameters(g3, 'Boost Pressure', 0, 80, 'PSI')
        
        g4= GaugeDigital()
        g4s= Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(620,80))
        GaugeDigital.setParents(g4,self,g4s)
        GaugeDigital.setGuageParameters(g4, 'Engine Load', 0, 80, 'Percent')
        g4s.add_widget(g4)
        
        """
        
        #Create header
        head = Header()

        #Create footer and schedule clock and date functions
        foot = Footer()
        Footer.updatedate(foot)
        Clock.schedule_interval(partial(Footer.updatetime, foot), 1)
        Clock.schedule_interval(partial(Footer.updatedate, foot), 3600)
        
        
        #Add Background Header and Footer
        self.appLayout.add_widget(self.bg)
        self.appLayout.add_widget(head)
        self.appLayout.add_widget(foot)


        #Add Menus
        self.settingMenu = Settings(size_hint=(.3,.01))
        self.gaugeMenu = AddGauge()
        head.add_widget(self.settingMenu)
        head.add_widget(self.gaugeMenu) #DONT MOVE, GETS FUCKED REAL QUICK
        
        #Add Guages
        for ag in ActiveGauges:
            self.appLayout.add_widget(ag)

        
        #Change to default touchscreen resolution
        Window.size = (800,600)
        return self.appLayout
    
    
        
if __name__ == '__main__':
    DigiDashApp().run()
