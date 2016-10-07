from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.clock import Clock
import time


class Header(Widget):

    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.bg = Image(source='Images/StatusBar.png', size=(800,80))
        self.add_widget(self.bg)
        self.drop = Header.genDropdown(self)    
        self.add_widget(self.drop)
        self.blutooth = Image(source='Images/blutooth.png', pos=(580,15), size=(50,55))
        self.add_widget(self.blutooth)
        self.drop = Header.settingDropdown(self)
        self.add_widget(self.drop)
        self.size = self.bg.size




#    def genDropdown(self):
#        """
#            Fuction to be used to add possible gauge values from file. 
#       """
#        Values= ['Calculated Engine Load',
#                 'Fuel Pressure',
#                 'Engine RPM',
#                 'Vehicle Speed',
#                 'MAF air flow rate',
#                 'Throttle position',]


#        codetype = DropDown()

#        for x in Values:
#            cur = Button(text=x, height=40, width=250)
            #cur.bind(on_release=lambda cur: codetype.select(cur.text))
#            codetype.add_widget(cur)

        
#        mainbutton = Button(text='Add New Gauge', height=40, width=250, pos=(20,20))
        #mainbutton = Button(text='Add New Gauge', size_hint = (None, None))
#        mainbutton.bind(on_release=codetype.open)
#        codetype.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #runTouchApp(mainbutton)

#        return mainbutton

        
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
        
        
        settingbutton = Button(text='Settings',height=40, width=160, pos=(630,20))
        settingbutton.bind(on_release=setmenu.open)
        setmenu.bind(on_select=lambda instance, x:setattr(settingbutton, 'text', a))
        
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
            

        mainbutton = Button(text='New Gauge', height=44, width=250, pos=(20,20))
        mainbutton.bind(on_release=codetype.open)
        codetype.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        #runTouchApp(mainbutton)

        return mainbutton 



    
        
