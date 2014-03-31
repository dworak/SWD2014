from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, ObjectProperty
from kivy.garden.graph import Graph
from kivy.uix.textinput import TextInput

Builder.load_string("""
<GraphScreen>:
    BoxLayout:
        Graph:
            id:graph
            xlabel:'X'
            ylabel:'Y'
            x_ticks_minor:1
            x_ticks_major:10
            y_ticks_major:10
            y_grid_label:True
            x_grid_label:True 
            padding:5
            x_grid:True
            y_grid:True
            xmin:-0
            xmax:100
            ymin:0
            ymax:100
            widht:300
            
<Console>:
    ScrollView:
        id: scrlv
        TextInput:
            id:console
            text:'test'
            background_color: [0, 0, 0, 0.5]
            foreground_color: [1, 1, 1, 1]
            size_hint: 1, None
            height: max( (len(self._lines)+1) * self.line_height, scrlv.height)
""")

class GraphScreen(Screen):
    graph = ObjectProperty(Graph)
    
    def __init__(self):
        super(GraphScreen, self).__init__()
        
    def getGraph(self):
        return self.ids.graph
    
class Console(Screen):
    console = ObjectProperty(TextInput)
    
    def __init__(self):
        super(Console, self).__init__()
    
    def getConsole(self):
        return self.ids.console
    