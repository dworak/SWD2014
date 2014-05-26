from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, ObjectProperty
from kivy.garden.graph import Graph
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.accordion import Accordion
from multiprocessing import Pool
from console import *
import json


class CarouselItem():
    DYSKRETYZACJA           = 0
    DYSKRETYZACJAMAXCOUNT   = 1
    STANDARYZACJA           = 2
    STANDARYZACJAMINMAX     = 3
    KLASYFIKACJAKNN         = 4 
    

#http://stackoverflow.com/questions/20181250/changing-the-background-color-of-a-button-in-kivy

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
    BoxLayout:
        orientation: 'vertical'
        spacing: 5
        BoxLayout:
            orientation: 'horizontal'
            size_hint:(1, 0.6)
            Accordion:
                id: carousel
                loop: True
                AccordionItem:
                    id: a
                    title:'Dyskretyzacja'
                    Spinner:
                        id: ilosc_przedzialow_a
                        text: "Liczba przedzialow"
                        values:(str(x) for x in range(0,100,5))
                    Spinner:
                        id: kolumna_a
                        text: "Parametr"
                        values:(str(x) for x in range(0,100))
                AccordionItem:
                    id: b
                    title:'Dyskretyzacja\\n(MaxCount)'
                    Spinner:
                        id: ilosc_przedzialow_b
                        text: "Liczba przedzialow"
                        values:(str(x) for x in range(0,100,5))
                    Spinner:
                        id: kolumna_b
                        text: "Parametr"
                        values:(str(x) for x in range(0,100))
                AccordionItem:
                    id: c
                    title:'Standaryzacja\\n(normalizacja)'
                    Spinner:
                        id: kolumna_c
                        text: "Kolumna"
                        values: (str(x) for x in range(0,100))
                AccordionItem:
                    id: d
                    title:'Standaryzacja\\n(MinMax)'
                    Spinner:
                        id: kolumna_d
                        text: "Kolumna"
                        values:(str(x) for x in range(0,100))
                    BoxLayout:
                        padding:  [10, 0, 10, 0]
                        orientation: 'vertical'
                        Slider:
                            step: 1
                            id: slider1
                            min: 0
                            max: 100
                        Label:
                            text: str(slider1.value)
                        Slider:
                            step: 1
                            id: slider2
                            min: 0
                            max: 100
                        Label:
                            text: str(slider2.value)
                AccordionItem:
                    id: e
                    title:'Klasyfikacja k-nn'
                    Spinner:
                        id: dostepne_metryki
                        text: "Parametr klasy decyzyjnej"
                        values:('Manhattan', 'Euclidesa', 'Mahalanobisa')
            Button:
                id: dyskretyzacja_przetwarzaj
                text: "Przetwarzaj"
                on_press: root.poinformuj_kontroler()
        KivyConsole:
            id: console
""")

class GraphScreen(Screen):
    graph = ObjectProperty(Graph)
    
    def __init__(self):
        super(GraphScreen, self).__init__()
        
    def getGraph(self):
        return self.ids.graph
    
class Console(Screen):
    console = ObjectProperty(KivyConsole)
    carousel = ObjectProperty(Accordion)
    accordionItems = []
    
    def __init__(self, app=None):
        super(Console, self).__init__()
        if app: self.app = app
        self.ids.kolumna_a.bind(text=self.spinner_value_changed)
        self.ids.kolumna_b.bind(text=self.spinner_value_changed)
        self.ids.kolumna_c.bind(text=self.spinner_value_changed)
        self.ids.kolumna_d.bind(text=self.spinner_value_changed)
        self.ids.ilosc_przedzialow_a.bind(text=self.spinner_value_changed)
        self.ids.ilosc_przedzialow_b.bind(text=self.spinner_value_changed)
        
        self.accordionItems.append(self.ids.a)
        self.accordionItems.append(self.ids.b)
        self.accordionItems.append(self.ids.c)
        self.accordionItems.append(self.ids.d)
        self.accordionItems.append(self.ids.e)
        
    def getConsole(self):
        return self.ids.console
    
    def getAccordion(self):
        return self.ids.carousel
    
    def current_expanded(self):
        for i in self.accordionItems:
            if i.collapse == False:
                return self.accordionItems.index(i)
    
    def spinner_value_changed(self,spinner, value):
        print value
        self.value = int(value)
        self.kolumna = int(value)
            
    def poinformuj_kontroler(self):
        pool = Pool(processes=1)
        index = self.current_expanded()

        if index == CarouselItem.DYSKRETYZACJA:
            try:
                if(self.app):
                    self.app.console.getConsole().stdout.write(json.dumps(self.app.sharedInstance.data.discretization(self.value, self.kolumna),  indent=4))
            except AttributeError:
                popup = Popup(title='Brak argumentow',content=Label(text='Dokonaj wyboru parametrow'),size_hint=(None, None), size=(500, 150))
                popup.open()
        elif index == CarouselItem.DYSKRETYZACJAMAXCOUNT:
            try:
                if(self.app):
                    self.app.console.getConsole().stdout.write(json.dumps(self.app.sharedInstance.data.discretizationMaxCount(self.value, self.kolumna),  indent=4))
            except AttributeError:
                popup = Popup(title='Brak argumentow',content=Label(text='Dokonaj wyboru parametrow'),size_hint=(None, None), size=(500, 150))
                popup.open()
        elif index == CarouselItem.KLASYFIKACJAKNN:
            pass
        elif index == CarouselItem.STANDARYZACJA:
            try:
                nazwa_kolumny = self.app.sharedInstance.data.temp[self.kolumna]
                wartosci = self.app.sharedInstance.data.normalizacja(nazwa_kolumny)
                if(self.app):
                    self.app.console.getConsole().stdout.write(json.dumps(wartosci,indent=4))
            except AttributeError:
                popup = Popup(title='Brak argumentow',content=Label(text='Dokonaj wyboru parametrow'),size_hint=(None, None), size=(500, 150))
                popup.open()
        elif index == CarouselItem.STANDARYZACJAMINMAX:
            try:
                nazwa_kolumny = self.app.sharedInstance.data.temp[self.kolumna]
                wartosci = self.app.sharedInstance.data.normalizacjaMinMax(nazwa_kolumny,self.ids.slider1.value, self.ids.slider2.value)
                if(self.app):
                    self.app.console.getConsole().stdout.write(json.dumps(wartosci,indent=4))
            except AttributeError:
                popup = Popup(title='Brak argumentow',content=Label(text='Dokonaj wyboru parametrow'),size_hint=(None, None), size=(500, 150))
                popup.open()
            
    