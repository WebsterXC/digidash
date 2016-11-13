# Graph data using the Graph module from Kivy Garden

import kivy
kivy.require('1.8.0')
  
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.garden.graph import Graph, MeshLinePlot
from math import sin
 
class AccelerometerDemo(BoxLayout):
    def __init__(self):
        super(AccelerometerDemo, self).__init__()
  
	#self.graph = self.ids.graph_plot

	graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5, x_ticks_major=25, y_ticks_major=1, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
	
	self.plot = MeshLinePlot(color=[1, 0, 0, 1])
	self.plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
	self.graph.add_plot(plot)
 
class AccelerometerDemoApp(App):
    def build(self):
        return AccelerometerDemo()
  
class ErrorPopup(Popup):
    pass
  
if __name__ == '__main__':
    AccelerometerDemoApp().run()
