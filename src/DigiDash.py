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
import ConfigParser


class DigiDashApp(App):
    def build(self):

        Config = ConfigParser.ConfigParser()
        Config.read("Settings.ini")
        GaugeList= Config.sections()[1:]

        self.ActiveGauges=[]

        #Initialize all Gauges from INI config file
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

            #print(g)
            #print(gtype,gstyle,gposx,gposy,gscale,gmeasure,gunits,gmin,gmax)


            if(gtype == 'analog'):
                curG = Gauge()
                curGS = Scatter(scale=gscale, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                Gauge.setParents(curG,self,curGS)
                Gauge.setGaugeParameters(curG, gmeasure, gmin, gmax, gunits)
                self.ActiveGauges.append(curGS)

		Clock.schedule_interval(partial(Gauge.setVALUE, curG), 0.0625)

            else:
                curG = GaugeDigital()
                curGS = Scatter(scale=gscale, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                GaugeDigital.setParents(curG,self,curGS)
                GaugeDigital.setGaugeParameters(curG, gmeasure, gmin, gmax, gunits)
                self.ActiveGauges.append(curGS)
						
		Clock.schedule_interval(partial(GaugeDigital.setVALUE, curG), 0.0625)

        #Define application layout
        self.appLayout = FloatLayout(size=(800,600))

        #Background loaded from ini file
        bg_path = Config.get('Application_Settings','Background')
        self.bg = Image(source=bg_path, pos=(0,0), size=(Window.size[0],Window.size[1]))


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
        Settings.set_parent(self.settingMenu, self)
        self.gaugeMenu = AddGauge()
        head.add_widget(self.settingMenu)
        head.add_widget(self.gaugeMenu) #DONT MOVE, GETS FUCKED REAL QUICK

        #Add Gauges
        for ag in self.ActiveGauges:
            self.appLayout.add_widget(ag)


        #piself.bind(size=self.__resize__)
        #Change to default touchscreen resolution
        #Window.size = (800,600)
        return self.appLayout

    def on_resize(width,height):
        print('RESIZED:' + str(width) + ' ' + str(height))

    def __resize__(instance, val):
        print('RESIZE TRIGGERED: '+str(Window.size))
        Settings.__resize__(self.settingMenu)
        AddGauge.__resize__(self.gaugeMenu)
        Header.__resize__(self.head)
        Footer.__resize__(self.foot)



if __name__ == '__main__':
    DigiDashApp().run()
