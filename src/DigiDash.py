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
from Header import Header
from Footer import Footer
from kivy.uix.dropdown import DropDown
import time
from functools import partial

class DigiDashApp(App):
    def build(self):
        appLayout = FloatLayout(size=(800,600))

        bg = Image(source='Images/Metal2.jpg', pos=(0,0), size=(1500,840))

        g1= Gauge()
        g1s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(30,80))
        g1s.add_widget(g1)
        #Gauge.setBackground(g1,'Images/Guages/GuageHead3.png')
        
        
        g2= Gauge()
        g2s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(220,80))
        g2s.add_widget(g2)
        g2.setMPH(100)

        g3= Gauge()
        g3s = Scatter(scale=0.5, size_hint=(None,None), size=(400,400), pos=(420,80))
        g3s.add_widget(g3)
        
        
        head = Header()
        headscat = Scatter(size=head.size, pos=(0,530), do_translation=False)
        headscat.add_widget(head)

        foot = Footer()
        Footer.updatedate(foot)
        #Clock.schedule_interval(foot.updatetime, 1)
        Clock.schedule_interval(partial(Footer.updatetime, foot), 1)
        Clock.schedule_interval(partial(Footer.updatedate, foot), 3600)
        #footscat = Scatter(size=foot.size, pos=(0,-10), do_translation=False)
        #footscat.add_widget(foot)

        self.gaugeMenu = DigiDashApp.genDropdown(self)
        self.settingMenu = DigiDashApp.settingDropdown(self)
        
        appLayout.add_widget(bg)
        appLayout.add_widget(g1s)
        appLayout.add_widget(g2s)
        appLayout.add_widget(g3s)
        appLayout.add_widget(headscat)
        appLayout.add_widget(self.gaugeMenu)
        appLayout.add_widget(self.settingMenu)
        appLayout.add_widget(foot)
        
        Window.size = (800,600)
        return appLayout

    def settingDropdown(self):
    
        def bibutpress(instance):
            print('The button <%s> is being pressed' % instance.text)
        def bcbutpress(instance):
            print('The button <%s> is being pressed' % instance.text)
        def hfbutpress(instance):
            print('The button <%s> is being pressed' % instance.text)
        def conbutpress(instance):
            print('The button <%s> is being pressed' % instance.text)
            
        Values = ['Background Image','Background Color','Header/Footer Image','Connection']
        
        setmenu = DropDown()
        
        bibut = Button(text='Background Image', size_hint_y= None, height= 40)
        bibut.bind(on_release=bibutpress)
        setmenu.add_widget(bibut)
        bcbut = Button(text='Background Color', size_hint_y= None, height= 40)
        bcbut.bind(on_release=bcbutpress)
        setmenu.add_widget(bcbut)
        hfbut = Button(text='Header/Footer Color', size_hint_y= None, height= 40)
        hfbut.bind(on_release=hfbutpress)
        setmenu.add_widget(hfbut)
        conbut = Button(text='Connection', size_hint_y= None, height= 40)
        conbut.bind(on_release=conbutpress)
        setmenu.add_widget(conbut)
        
        
        settingbutton = Button(text='Settings',size_hint=(.20,.08), pos=(630,545))
        settingbutton.bind(on_release=setmenu.open)
        #setmenu.bind(on_select=lambda instance, x:setattr(settingbutton, 'text', a))
        
        return settingbutton
    
    def genDropdown(self):
        """
            Fuction to be used to add possible gauge values from file. 
        """
    
        Values= ['Engine Load',
                 'Fuel Pressure',
                 'Tachometer',
                'Speedometer',
                'MAF',
                'Throttle Pos',
                'Boost Pressure']


        codetype = DropDown()

        for x in Values:
            cur = Button(text=x, size_hint_y= None, height= 40)
            codetype.add_widget(cur)
            

        mainbutton = Button(text='New Gauge', size_hint=(.20,.08), pos=(20,545))
        mainbutton.bind(on_release=codetype.open)
        #codetype.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #runTouchApp(mainbutton)
        return mainbutton
        
if __name__ == '__main__':
    DigiDashApp().run()
