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
import ast
from functools import partial
import ConfigParser
import subprocess  

from can import pids

class DigiDashApp(App):
    def build(self):

        Config = ConfigParser.ConfigParser()
        Config.read("Settings.ini")
        GaugeList= Config.sections()[1:]

        self.ActiveGauges=[]
        
        bright = Config.get('Application_Settings','Brightness')
        subprocess.call(['sudo','./brightness.sh',str(bright)])

        #Initialize all Gauges from INI config file
        for g in GaugeList:
            gtype = Config.get(g,'type')
            gstyle = int(Config.get(g,'style'))
            gposx = float(Config.get(g,'posx'))
            gposy = float(Config.get(g,'posy'))
            gscale = float(Config.get(g,'scale'))
            gmeasure = Config.get(g,'measure')
            gunits = Config.get(g,'units')
            gmin = float(Config.get(g,'min'))
            gmax = float(Config.get(g,'max'))
            PID = str(Config.get(g, 'pid'))

            bg = Config.get(g,'background')
            tc = ast.literal_eval(str(Config.get(g,'textcolor')))
            dl = Config.get(g,'dialcolor')

            #print(g)
            #print(gtype,gstyle,gposx,gposy,gscale,gmeasure,gunits,gmin,gmax)


            if(gtype == 'analog'):
                curG = Gauge()
                curGS = Scatter(scale=gscale, scale_min=0.25, scale_max=1.5, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                Gauge.setParents(curG,self,curGS)
                Gauge.setGaugeParameters(curG, gmeasure, gmin, gmax, gunits)
                self.ActiveGauges.append(curGS)
                curG.gauge.source = bg
                curG.dial.source = dl

                for l in curG.UnitScaleLabels:
                    l.color = tc
                
                curG.MTitle.color = tc
                curG.MUnits.color = tc

                curG.PID = PID

                Clock.schedule_interval(partial(Gauge.setVALUE, curG), 0.0625)

            else:
                curG = GaugeDigital()
                curGS = Scatter(scale=gscale, scale_min=0.25, scale_max=1.5, size_hint=(None,None), size=(400,400), pos=(gposx,gposy))
                curGS.add_widget(curG)
                GaugeDigital.setParents(curG,self,curGS)
                GaugeDigital.setGaugeParameters(curG, gmeasure, gmin, gmax, gunits)
                self.ActiveGauges.append(curGS)
                curG.gauge.source = bg


                curG.MTitle.color = tc
                curG.MUnits.color = tc
                curG.VALUE.color = tc

                curG.PID = PID
                
                Clock.schedule_interval(partial(GaugeDigital.setVALUE, curG), 0.0625)

        #Define application layout
        self.appLayout = FloatLayout(size=(800,600))

        #Background loaded from ini file
        bg_path = Config.get('Application_Settings','Background')
        self.bg = Image(source=bg_path, pos=(0,0), size=(Window.size[0],Window.size[1]))


        #Create header
        #head = Header()
    #win_w = Window.size[0]
        #win_h = Window.size[1]
    #head = Image(source='Images/StatusBar.png', size=(win_w,win_h/12), pos=(0,win_h-60))

        #Create footer and schedule clock and date functions
        foot = Footer()
        Footer.updatedate(foot)
        Clock.schedule_interval(partial(Footer.updatetime, foot), 1)
        Clock.schedule_interval(partial(Footer.updatedate, foot), 3600)
    

        #Add Background Header and Footer
    #self.appLayout.add_widget(head)
        self.appLayout.add_widget(self.bg)
        self.appLayout.add_widget(foot)


        #Add Menus
        self.settingMenu = Settings(size_hint=(.3,.01))
        Settings.set_parent(self.settingMenu, self)
        self.gaugeMenu = AddGauge()
        AddGauge.set_parent(self.gaugeMenu, self)
        self.appLayout.add_widget(self.settingMenu)
        self.appLayout.add_widget(self.gaugeMenu) #DONT MOVE, GETS FUCKED REAL QUICK

        #Add Gauges
        for ag in self.ActiveGauges:
            self.appLayout.add_widget(ag)


        #piself.bind(size=self.__resize__)
        #Change to default touchscreen resolution
        #Window.size = (800,600)
        self.Config = Config #Create a class reff to Config Parser used in startup
        return self.appLayout

    def on_resize(width,height):
        print('RESIZED:' + str(width) + ' ' + str(height))

    def __resize__(instance, val):
        print('RESIZE TRIGGERED: '+str(Window.size))
        Settings.__resize__(self.settingMenu)
        AddGauge.__resize__(self.gaugeMenu)
        Header.__resize__(self.head)
        Footer.__resize__(self.foot)


    def close_all_gauge_menus(instance):
    	#Loops through all active gauges and closes menus that are open
    	for g in instance.ActiveGauges:
    		ga = g.children[0]
    		if ga.settings_open== True:
    			ga.close_menus()


    def save_settings(instance):
        confile = open("Settings.ini",'w') #might want to be one in home directory so ini doesnt write over in commits
        
        n = len(instance.ActiveGauges)
        c = len(instance.Config.sections())-1 #Number of gauge sections
        if(n<c):
            diff = c-(c-n)
            remove_sec = instance.Config.sections()[diff:]
            for sec in remove_sec:
                instance.Config.remove_section(sec)

        i=0 #COUNTER FOR SECTION NAME
        for ga in instance.ActiveGauges:
            g = ga.children[0]  #Get the gauge class from the scatter
            i+=1

            #DEFINITIONS FOR SAVING
            gname = 'Gauge_'+str(i)
            bg = g.gauge.source
            tc = g.MTitle.color
            if isinstance(g, Gauge):
                dl = g.dial.source
                tp = 'analog'
            else:
                dl = 'None'
                tp = 'digital'

            posx = ga.pos[0]
            posy = ga.pos[1]
            scale = ga.scale
            measure = g.Measure
            units = g.Units
            minv = g.MinValue
            maxv = g.MaxValue
            PID = g.PID


            #INI SECTION CREATION 
            if not instance.Config.has_section(gname):
                instance.Config.add_section(gname)
            
            #SET INI VALUES FROM VARIABLE
            instance.Config.set(gname,'type',tp)
            instance.Config.set(gname,'style',1)
            instance.Config.set(gname,'posx',posx)
            instance.Config.set(gname,'posy',posy)
            instance.Config.set(gname,'scale',scale)
            instance.Config.set(gname,'measure',measure)
            instance.Config.set(gname,'units',units)
            instance.Config.set(gname,'min',minv)
            instance.Config.set(gname,'max',maxv)
            instance.Config.set(gname,'pid', PID)
            instance.Config.set(gname,'background',bg)
            instance.Config.set(gname,'textcolor',tc)
            instance.Config.set(gname,'dialcolor',dl)

        instance.Config.write(confile)
        confile.close()


if __name__ == '__main__':
    DigiDashApp().run()
