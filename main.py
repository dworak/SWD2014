#project settings
import sys
sys.path.append("Logic")
sys.path.append("Views")
sys.path.append("LDGlobal")

#kivi main
from kivy.app import App
from kivy.config import Config
import kivy

#controls
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition,SlideTransition

#file browser
from kivy.garden.filebrowser import FileBrowser
from kivy.uix.popup import Popup
from os.path import sep, expanduser, isdir, dirname
from kivy.uix.modalview import ModalView

#plotting
from kivy.garden.graph import Graph, MeshLinePlot
from kivy.graphics import Color, Rectangle

from kivy.animation import Animation

from math import sin
import random
import pprint
from functools import partial

#data
from data import Data

#views
from views import *

#enum for presenting modal
class ModalTypes:
    FILE        = 1
    OBJECT      = 2
    ATTRIBUTE   = 3
    
class ManagerPlikow:
    
    def __init__(self):
        self.data = Data()

    def przegladajDysk(self):
        user_path = expanduser('~') + sep + 'Documents'
        browser = FileBrowser(select_string='Select',
                              favorites=[(user_path, 'Documents')])
        browser.bind(
                    on_success=self._fbrowser_success,
                    on_canceled=self._fbrowser_canceled)
        return browser

    def _fbrowser_canceled(self,instance):
        app.modalView.dismiss()
        print 'cancelled, Close self.'

    def _fbrowser_success(self,instance):
        path = instance.selection[0]
        if (path.lower().endswith(".csv")):
            
            self.zaladujModel(path)
            app.modalView.dismiss()
            app.buildCenterMenu(app.menuCenterWrapper, True)
        else:
            popup = Popup(title='Nieznany format pliku',content=Label(text='To nie jest plik csv'),size_hint=(None, None), size=(500, 150))
            popup.open()

    def zaladujModel(self,sciezka):
        import random
        self.data.loadFile(sciezka, app, wantSorted=True, index=0)
        for property in self.data.temp:
            r = lambda: random.randint(0,255)/255.0
            plot = MeshLinePlot(color=[r(), r(), r(), 1])
            
            points = []
            i = 0
            for object in self.data.data:
                try:
                    value = float(object[property])
                    points.append((i, value))
                except (ValueError, KeyError):
                    pass
                i+=1
            plot.points = points
            app.graphScreen.getGraph().add_plot(plot)
        
class Constant(object):
    def __init__(self, val, tag):
        super(Constant, self).__setattr__("value", val)
        super(Constant, self).__setattr__("tag", tag)
    def __setattr__(self, name, val):
        raise ValueError("Trying to change a constant value", self)

class SystemyWspomaganiaDecyzji(App):

    def __init__(self):
        super(SystemyWspomaganiaDecyzji,self).__init__()
        self.sharedInstance = ManagerPlikow()
        self.menuLeftWrapper = None;
        self.meuCenterWrapper = None;
        self.checkBoxesPlotBind = {}
    # def on_start(self):
        #Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, win, key, scancode, string, modifiers):
        print( win.size, key)
        if key == 102: # 'f'
            normalsize = [ Config.getint('graphics', 'width'), Config.getint('graphics', 'height') ]
            if (win._size == normalsize):
                win._size = [1440, 900]
            else:
                win._size = normalsize
                win.toggle_fullscreen()
                win.update_viewport()
        return True
        
    def getLeftWrapper(self):
        return self.me
    
    def pokazWyborPliku(self, animated, instance, *args):
        modalType = 1
        anim = None;
        
        #modal animation
        if(animated):
            anim = Animation(size=(640, 480), duration=0.5)
            
        #modal frame size
        size=(240, 160)
        if(anim==None):
            size = (640,480)
        else:
            #TODO:
            pass
            
        self.modalView = ModalView(size_hint=(None, None), size=size)
        self.modalView.add_widget(self.sharedInstance.przegladajDysk())
        
        #paramter in the method call, will perform some basic slace animation
        if(animated): 
            anim.start(self.modalView)
        self.modalView.open()
        
    def pokazDodanieAtrybutu(self):
        view = ModalView(size_hint=(None, None), size=(640, 480))
        view.open()
        return view
        
    def pokazDodanieObiektu(self, *args):
        view = ModalView(size_hint=(None, None), size=(640, 480))
        box = BoxLayout(orientation="vertical",spacing=10)
        scrollView = ScrollView(bar_margin=10, bar_color=[1,1,1,1])
        viewWrapper = GridLayout(cols=2, row_default_height=40,size_hint_y=None,padding=[-20,20,20,20])
        viewWrapper.bind(minimum_height=viewWrapper.setter('height'))
        
        listaTextBoxow = []
        
        for i in range(len(self.sharedInstance.data.temp)):
            l = Label(text=self.sharedInstance.data.temp[i],halign="left", width=50)
            #textPlaceHolder = 'Tutaj wpisz wartosc dla {0}'.format(self.sharedInstance.data.temp[i])
            #textPlaceHolder,multiline=False,  )
            textinput = TextInput(multiline=False, text="0",focus=True) 
            listaTextBoxow.append(textinput)
            viewWrapper.add_widget(l)
            viewWrapper.add_widget(textinput)
            #background_color=[51/255.0, 181.0/255, 229/255.0,1]
        scrollView.add_widget(viewWrapper)
        box.add_widget(scrollView)
        box.add_widget(Button(text='Dodaj', font_size=14, on_press=partial(self.dodajObiekt,view, listaTextBoxow), size_hint=(1, .1)))
        view.add_widget(box)
        view.open()
        return view
    
    def dodajObiekt(self,view,lista,*args):
        self.sharedInstance.data.dodajNowyWiersz([element.text for element in lista])
        view.dismiss()
        
    def setOrientation(self, orient):
        self.orient = orient
        
    def onPressCallback(self,instance):
        self.pokazWyborPliku(instance,False)
        
    def onPressGraphConsoleSwitch(self,instance):
        if(instance.text=="Konsola"):
            instance.text = "Graf"
            self.sm.switch_to(self.console, direction='up')
        elif(instance.text=="Graf"):
            instance.text = "Konsola"
            self.sm.switch_to(self.graphScreen, direction='down')
          
    def checkBoxCallback(self,instance,value, *args):
        if(value==False):
            self.graphScreen.getGraph().remove_plot(app.checkBoxesPlotBind[instance])
        else:
            self.graphScreen.getGraph().add_plot(app.checkBoxesPlotBind[instance])
        self.graphScreen.getGraph()._redraw_all
        
    def buttonCallback(self, instance):
        for plot in self.graphScreen.getGraph().plots:
            plot.points = []
            
        poNormalizacji = {}
        for property in self.sharedInstance.data.temp:
            poNormalizacji[property] = self.sharedInstance.data.normalizacja(property)
            
        for property in poNormalizacji:
            points = []
            lista = poNormalizacji[property]
            i, j = 0
            pprint.pprint(lista)
            for j in range(len(lista)):
                points.append((i,lista[j]))
                i+=1
            pprint.pprint(points)
#             for plot in self.graph.plots:
#                 plot.points = points
            
        self.graph.ymax = 10
        self.graph.ymin = -10
            
        
    def buildCenterMenu(self, wrapper, rebuild=False):
        if(rebuild): wrapper.clear_widgets()
        
        numberOfItems = len(self.sharedInstance.data.temp) if self.sharedInstance.data.temp else 0
        for i in range(0, numberOfItems):
            checkbox = CheckBox(active=True)
            checkbox.bind(active=app.checkBoxCallback)
            self.checkBoxesPlotBind[checkbox] = self.graphScreen.getGraph().plots[i]
            
            labelText = self.sharedInstance.data.temp[i] if self.sharedInstance.data.temp else "Nazwa atrybutu"
            label = Label(text=labelText, halign = "right",width=100, col_default_width=20, col_force_default=True)
            wrapper.add_widget(label)
            wrapper.add_widget(checkbox)
            
    def buildLeftMenu(self, wrapper):
        buttonWybierzPlik = Button(text='Wczytaj plik', font_size=14)
        buttonWybierzPlik.bind(on_press=partial(self.pokazWyborPliku,False))
        wrapper.add_widget(buttonWybierzPlik)
        
        buttonDodajObiekt = Button(text='Dodaj obiekt', font_size=14)
        buttonDodajObiekt.bind(on_press=partial(self.pokazDodanieObiektu))
        wrapper.add_widget(buttonDodajObiekt)
        
        buttonDodajAtrybut = Button(text='Dodaj atrybut', font_size=14)
        buttonDodajAtrybut.bind(on_press=self.onPressCallback)
        wrapper.add_widget(buttonDodajAtrybut)
        
        buttonStatystyki = Button(text='Statystyki', font_size=14)
        buttonStatystyki.bind(on_press=self.onPressCallback)
        wrapper.add_widget(buttonStatystyki)
        
        buttonKonsola = Button(text='Graf', font_size=14)
        buttonKonsola.bind(on_press=self.onPressGraphConsoleSwitch)
        wrapper.add_widget(buttonKonsola)  
        
    def sliderValueChanged(self,label,description,slider,*args):
        if(description.tag==1):
            self.graphScreen.getGraph().x_ticks_major = 100//args[0] if args[0]!=0.0 else 100
            label.text = "{0} {1}".format(description.value,int(args[0]))
        elif(description.tag==2):
            if(int(args[1])<self.graphScreen.getGraph().xmax):
                self.graphScreen.getGraph().xmin = int(args[1])
                label.text = "{0} {1}".format(description.value,int(args[1]))
                args[0].max = slider.value
        elif(description.tag==3):
            if(int(args[1])>self.graphScreen.getGraph().xmin):
                self.graphScreen.getGraph().xmax = int(args[1])
                label.text = "{0} {1}".format(description.value,int(args[1]))
                args[0].min = slider.value
        elif(description.tag==4):
            self.graphScreen.getGraph().x_ticks_major = int(args[0])
            label.text = "{0} {1}".format(description.value,int(args[0]))
        else:
            raise ValueError("Wrong tag of the slider, check it.", self)
        
        self.graphScreen.getGraph()._redraw_all()
    
        
    def build(self):
        
        self.sm = ScreenManager(transition=SlideTransition())
        layout = BoxLayout(padding=20, orientation=self.orient, spacing=20)

        self.graphScreen = GraphScreen()

        self.console = Console(app=app)
        
        self.sm.switch_to(self.console)
        
        self.graph = self.graphScreen.getGraph();
        
        layout.add_widget(self.sm)

        menuWrapper = BoxLayout()
        
        for i in range(0,3):            
            #pragma mark boczne menu z lewej
            if(i==0):
                menuInside = BoxLayout(orientation="vertical")
                self.meuCenterWrapper = menuInside;
                self.buildLeftMenu(menuInside)
                menuWrapper.add_widget(menuInside)
                
            #srodkowa czesc
            if(i==1):
                scrollView = ScrollView(bar_margin=10, bar_color=[1,1,1,1])
                #pragma mark padding narzucony w srodkowym menu
                menuInside = GridLayout(cols=4, row_default_height=40,size_hint_y=None,padding=[50,0,0,0])
                menuInside.bind(minimum_height=menuInside.setter('height'))
                self.menuCenterWrapper = menuInside;
                self.buildCenterMenu(menuInside)
                scrollView.add_widget(menuInside)
                menuWrapper.add_widget(scrollView)
                    
            #menu po prawej
            if(i==2):
                menuInside = BoxLayout(orientation="vertical")
                gridWrapper = GridLayout(cols=2)
                #liczba przedzialow
                s = Slider(min=0, max=10, value=5, step=1)
                s.value = 10
                numberOfIntervalsBaseString = Constant("Liczba przedzialow:",1)
                textNumberOfIntervalsBaseString = "{0} {1}".format(numberOfIntervalsBaseString.value, s.value)
                l = Label(text=textNumberOfIntervalsBaseString, halign="center")
                gridWrapper.add_widget(l)
                s.bind(value=partial(self.sliderValueChanged,l,numberOfIntervalsBaseString))
                gridWrapper.add_widget(s)
                
                #wartosc min delklaracja
                minSlider = Slider(min=0, max=100, value=5, step=1)
                #wartosc max deklaracja
                maxSlider = Slider(min=0, max=100, value=5, step=1)
                
                #wartosc min cd
                minSlider.value = 0
                textMinBaseString = Constant("Wartosc min\nuzytkownika:",2)
                textMinString = "{0} {1}".format(textMinBaseString.value, minSlider.value)
                min = Label(text=textMinString, halign="center")
                gridWrapper.add_widget(min)
                minSlider.bind(value=partial(self.sliderValueChanged,min,textMinBaseString, maxSlider))
                gridWrapper.add_widget(minSlider)
                
                #wartosc max cd
                maxSlider.value = 100
                textMaxBaseString = Constant("Wartosc max\nuzytkownika:",3)
                textMaxString = "{0} {1}".format(textMaxBaseString.value, maxSlider.value)
                max = Label(text=textMaxString, halign="center")
                gridWrapper.add_widget(max)
                maxSlider.bind(value=partial(self.sliderValueChanged,max,textMaxBaseString, minSlider))
                gridWrapper.add_widget(maxSlider)
                
                #skok dla przedzialu
                s = Slider(min=0, max=10, value=5, step=.1)
                s.value = 0
                textJumpBaseString = Constant("Szerokosc przedzialu:",4)
                textJump = "{0} {1}".format(textJumpBaseString.value, s.value_normalized)
                j = Label(text=textJump, halign="left")
                s.bind(value=partial(self.sliderValueChanged,j,textJumpBaseString))
                gridWrapper.add_widget(j)
                gridWrapper.add_widget(s)
                
                # Normalizacja zmiennych rzeczywistych ( (wartosc-srednia)/odchylenie_standardowe)
                b = Button(text="Normalizacja danych", on_press=self.buttonCallback)
                gridWrapper.add_widget(b)
                
                
                z = Button(text="Zamiana danych tekstowych\nna numeryczne",  halign='center')
                gridWrapper.add_widget(z)

                menuInside.add_widget(gridWrapper);
                menuWrapper.add_widget(menuInside)
            
        layout.add_widget(menuWrapper)
        return layout
    
if __name__ == "__main__":
    from kivy.core.window import Window
    Window.clearcolor = (.64,.64,.64, 1)
    Window._size = [1440, 791]
    app = SystemyWspomaganiaDecyzji()
    app.setOrientation(orient="vertical")
    print Window.size
    app.run()
