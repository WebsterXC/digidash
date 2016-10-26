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
from GaugeClass import Gauge
from GaugeClassDigital import GaugeDigital
from Settings import Settings
from AddGauge import AddGauge
from Header import Header
from Footer import Footer
from kivy.uix.dropdown import DropDown
import time
from functools import partial

class DigiDashApp(App):
    def build(self):
        #Define application layout
        appLayout = FloatLayout(size=(800,600))

        #Create initial background, replace eventually with settings load from ini file
        bg = Image(source='Images/Metal2.jpg', pos=(0,0), size=(1500,840))
        
        #Create all initial guages, switch eventually to load from settings ini file
        g1= Gauge()
        g1s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(30,80))
        g1s.add_widget(g1)
        Gauge.setGuageParameters(g1, 'Speedometer', 0, 80, 'MPH')
        #Gauge.setBackground(g1,'Images/Guages/GuageHead3.png')
        
        g2= Gauge()
        g2s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(220,80))
        g2s.add_widget(g2)
        Gauge.setGuageParameters(g2, 'Fuel Pressure', 0, 80, 'PSI')
        g2.setMPH(100)

        g3= Gauge()
        g3s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(420,80))
        g3s.add_widget(g3)
        Gauge.setGuageParameters(g3, 'Boost Pressure', 0, 80, 'PSI')
        
        
        #Create header
        head = Header()

        #Create footer and schedule clock and date functions
        foot = Footer()
        Footer.updatedate(foot)
        Clock.schedule_interval(partial(Footer.updatetime, foot), 1)
        Clock.schedule_interval(partial(Footer.updatedate, foot), 3600)
        
        
        #Add Background Header and Footer
        appLayout.add_widget(bg)
        appLayout.add_widget(head)
        appLayout.add_widget(foot)


        #Add Menus
        self.settingMenu = Settings(size_hint=(.3,.01))
        self.gaugeMenu = AddGauge()
        head.add_widget(self.settingMenu)
        head.add_widget(self.gaugeMenu) #DONT MOVE, GETS FUCKED REAL QUICK
        
        #Add Guages
        appLayout.add_widget(g1s)
        appLayout.add_widget(g2s)
        appLayout.add_widget(g3s)
        
        #Change to default touchscreen resolution
        Window.size = (800,600)
        return appLayout

    
        
if __name__ == '__main__':
    DigiDashApp().run()
