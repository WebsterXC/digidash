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
from can import canbus, daemon


class GaugeDigital(Widget):
	def __init__(self, **kwargs):
		super(GaugeDigital, self).__init__(**kwargs)

		#REF TO MAIN CLASS
		self.Parent = None
		self.Scat = None;

		#GAUGE SPECIFIC VALUES
		self.Measure = 'DEFAULT'
		self.MinValue = 0
		self.MaxValue = 80
		self.Units = 'DEF'
		self.PID = None #ADD THIS VALUE TO setGaugeParameters

		#BACKGROUND
		self.gauge = Image(source='Images/Gauges/GaugeSquare1.png', size=(400, 400))
		self.style = 1

		#GAUGE VALUE
		self.VALUE = Label(text='0', font_size='120sp', pos=(150, 160), color=(0, 0, 0, 1))

		#SETTINGS MENU BUTTON
		self.settings = Button(text='Modify', pos=(155, 40), size=(80, 30), color=(51, 102, 255, 1))
		self.settings.bind(on_release=self.menu)
		self.settings_open = False

		#REF TO MENU
		self.gmenu = None

		#GAUGE MEASUREMENTS AND UNTIS
		self.MTitle = Label(text=self.Measure, font_size='26sp', pos=(150, 40), color=(0, 0, 0, 1))
		self.MUnits = Label(text=self.Units, font_size='22sp', pos=(150, 70), color=(0, 0, 0, 1))


		#ADDING TO WIDGET
		self.add_widget(self.gauge)
		self.add_widget(self.settings)
		self.add_widget(self.MTitle)
		self.add_widget(self.MUnits)
		self.add_widget(self.VALUE)

	"""
	_____________________________________________________________
	|                                                            |
	|                    MENU CREATION FUNCTIONS                 |
	|                                                            |
	|    THESE FUCNTIONS CREATE GAUGE CUSTOMIZATION MENUS        |
	|    MENUS INCLUDE:                                          |
	|        MAIN MENU (menu)                                    |
	|            -THEME MENU    (preset_themes_menu)             |
	|            -GAUGE BACKGROUND MENU (gauge_background_menu)  |
	|            -GAUGE DIAL MENU (gauge_dial_menu)              |
	|            -GAUGE RIM MENU								 |
	|            _TEXT COLOR MENU								 |
	|____________________________________________________________|
	"""

	def menu(self, *largs):
		"""
			Creates a menu to modify gauge style
		"""
		if(self.settings_open == False):
			menu = BoxLayout(
						size_hint=(0.25, (0.05*7)),
						orientation='vertical')

			PST = Button(text='Preset Themes')
			PST.bind(on_release=self.preset_themes_menu)

			GBG = Button(text='Gauge Background')
			GBG.bind(on_release=self.gauge_background_menu)

			GTC = Button(text='Text Color')
			GTC.bind(on_release=self.gauge_text_menu)

			delete = Button(text='[ --- DELETE --- ]')
			delete.bind(on_release=self.deleteGauge)

			close = Button(text='[ CLOSE ]')
			close.bind(on_release=self.close_menus)

			menu.add_widget(PST)
			menu.add_widget(GBG)
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
		"""
			Changes background image of gauge
		"""
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


	def gauge_text_menu(self, *largs):
		"""
			Changes font color of gauge
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
	____________________________________________________________
	|                                                            |
	|                    GAUGE UTILITY FUNCTIONS                 |
	|                                                            |
	|____________________________________________________________|
	"""
	def setVALUE(self, *largs):
		"""
			Actually sets the value of the current gauge
		"""
		#self.VALUE.text= val
		#print(canbus.CANdata["0x0C"])
		#SHOULD BE:
		#self.VALUE.text = str(canbus.CANdata[self.PID])
		#FOR TESTING USE:
		self.VALUE.text = str(canbus.CANdata[0x0C])

	def setParents(self, P, S):
		"""
			Sets the parent and scatter for the current gauge
		"""
		self.Parent = P
		self.Scat = S

	def setGaugeParameters(self, Meas, Min, Max, UnitM):
		"""
			Defines all required gauge parameters
		"""
		#ADD PID VALUE
		self.Measure = Meas
		#UPDATE TEXT
		self.MTitle.text = Meas
		self.Units = UnitM
		self.MUnits.text = UnitM

	def back_to_menu(self, *largs):
		"""
			Closes current open menu and re-opens main menu
		"""
		self.close_menus()
		self.menu()

	def close_menus(self, *largs):
        	"""
            		Closes open menu
       		 """
        	self.Parent.appLayout.remove_widget(self.gmenu)
        	self.settings_open = False
        	self.settings.text = 'Modify'

	def setBackground(self, imagesrc, *largs):
		"""
			Helper function to change background image source of gauge
		"""
        	self.gauge.source = imagesrc

	def deleteGauge(self, *largs):
		"""
			Gauges are stored in the scatter in the main class in both the active gauge list
        	and the appLayout visually. Remove from both to delete current gauge
		"""
        	#self.Parent.ActiveGauges.remove(self.Scat)
        	self.Parent.appLayout.remove_widget(self.Scat)


	"""
	 ____________________________________________________________
	|                                                            						|
	|                    THEME FUNCTIONS                        			|
	|                                                            |
	|    THEME DEFINES BACKGROUND, DIAL, FONT COLOR, AND RIM     |
	|                                                            |
	|____________________________________________________________|
	""" 

	def style_1(self, *largs):
		""" Theme style 1 """
		self.setBackground('Images/Gauges/GaugeSquare1.png')
		self.MTitle.color = (0, 0, 0, 1)
		self.MUnits.color = (0, 0, 0, 1)
		self.VALUE.color = (0, 0, 0, 1)

	def style_2(self, *largs):
		""" Theme style 2 """
		self.setBackground('Images/Gauges/GaugeSquare2.png')
		self.MTitle.color = (1, 1, 1, 1)
		self.MUnits.color = (1, 1, 1, 1)
		self.VALUE.color = (1, 1, 1, 1)

	def style_3(self, *largs):
		""" Theme style 3 """
		self.setBackground('Images/Gauges/GaugeSquare3.png')
		self.MTitle.color = (1, 1, 1, 1)
		self.MUnits.color = (1, 1, 1, 1)
		self.VALUE.color = (1, 1, 1, 1)

	def style_4(self, *largs):
		""" Theme style 4 """
		self.setBackground('Images/Gauges/GaugeSquare4.png')
        	self.MTitle.color = (0, 0, 0, 1)
        	self.MUnits.color = (0, 0, 0, 1)
        	self.VALUE.color = (0, 0, 0, 1)

	def style_5(self, *largs):
		""" Theme style 5 """
        	self.setBackground('Images/Gauges/GaugeSquare5.png')
        	self.MTitle.color = (1, 1, 1, 1)
        	self.MUnits.color = (1, 1, 1, 1)
        	self.VALUE.color = (1, 1, 1, 1)

	def style_6(self, *largs):
		""" Theme style 6 """
        	self.setBackground('Images/Gauges/GaugeSquare6.png')
        	self.MTitle.color = (0, 0, 0, 1)
        	self.MUnits.color = (0, 0, 0, 1)
        	self.VALUE.color = (0, 0, 0, 1)

	def style_7(self, *largs):
		""" Theme style 7 """
        	self.setBackground('Images/Gauges/GaugeSquare7.png')
        	self.MTitle.color = (1, 1, 1, 1)
        	self.MUnits.color = (1, 1, 1, 1)
		self.VALUE.color = (1, 1, 1, 1)


	"""
	____________________________________________________________
	|                                                            |
	|                    BACKGROUND FUNCTIONS                    |
	|                                                            |
	|    THESE FUNCTIONS ONLY CHANGE BACKGROUND IMAGES SOURCE    |
	|                                                            |
	|____________________________________________________________|
	"""

	def bg_1(self, *largs):
		""" Background 1 """
		# Gauge Background Image [WHITE]
		self.setBackground('Images/Gauges/GaugeSquare1.png')

	def bg_2(self, *largs):
		""" Background 2 """
		# Gauge Background Image []
		self.setBackground('Images/Gauges/GaugeSquare2.png')

	def bg_3(self, *largs):
		""" Background 3 """
		self.setBackground('Images/Gauges/GaugeSquare3.png')

	def bg_4(self, *largs):
		""" Background 4 """
		self.setBackground('Images/Gauges/GaugeSquare4.png')

	def bg_5(self, *largs):
		""" Background 5 """
		self.setBackground('Images/Gauges/GaugeSquare5.png')
 
	def bg_6(self, *largs):
		""" Background 6 """
		self.setBackground('Images/Gauges/GaugeSquare6.png')

	def bg_7(self, *largs):
		""" Background 7 """
		self.setBackground('Images/Gauges/GaugeSquare7.png')


	"""
	_____________________________________________________________
	|                                                            |
	|                    TEXT FUNCTIONS                          |
	|                                                            |
	|       THESE FUNCTIONS ONLY CHANGE FONT COLOR OF GAUGES     |
	|                                                            |
	|____________________________________________________________|
	"""

	def black_font(self, *largs):
		"""
			Change font to the color black
		"""
		#String Identifiers
		self.MTitle.color = (0, 0, 0, 1)
		self.MUnits.color = (0, 0, 0, 1)

	def white_font(self, *largs):
		"""
			Change font to the color white
		"""
		#String Identifiers
		self.MTitle.color = (1, 1, 1, 1)
		self.MUnits.color = (1, 1, 1, 1)
