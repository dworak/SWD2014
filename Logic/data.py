import csv
import array
import string
import operator
import itertools
import collections
from operator import itemgetter

from sys import maxint
from metryka import Metryka
from numpy.numarray.numerictypes import MAX_INT_SIZE

#statistics
from sklearn.cross_validation import LeaveOneOut

class MetrykaValues:
    MANHATAN      = 1
    EUCLIDES      = 2
    MAHALANOBIS   = 3

class Data:
    
    def __init__(self):
        self.data = []
        self.temp = []
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Data, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
    #jesli chcemy wczytac dane od razu posortowane po odpowiedniej kolumnie dodaj parametr nadpisujacy domyslnie sorted i column
    def loadFile(self, sciezka, app=None, index=-1, wantSorted=False):
        with open(sciezka, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            
            listAttributes = None;
            
            if wantSorted == True and index>=0:
                reader = list(reader)
                listAttributes = reader[0]
                reader = sorted(reader[1:], key=operator.itemgetter(index))
                reader.insert(0, listAttributes)
            
            for row in reader:
                dict = {}
                if (row[0][0].startswith('#')==False):
                    if len(self.temp)<len(row):
                        for word in row:
                            self.temp.append(word)
                    else:
                        for i in range(0, len(row)):
                            dict[self.temp[i]] = row[i]
                        self.data.append(dict)
                else:
                    pass
            text = "\n".join([str(i) for i in reader])
            
            if(app):
                app.console.getConsole().text=text
                
    def zamianaWartosciTekstowychNaWartosciLiczbowe(self):
        zamiana = {}
        j = 0
        
        if self.data==None:
            assert self.data, "You should load data file first."
        
        for lista in self.data:
            print lista
            for i in lista:
                if(type(lista[i]) is str):
                    if(str(i) in zamiana):
                        zamiana[str(i)] = j
                        lista[str(i)] = j
                        j+=1
                    else:
                        lista[str(i)] = zamiana[str(i)]
                else:
                    pass #correct -> not string value
                    
                        
    def zwrocWszystkieWiersze(self):
        return self.data
            
    def zwrocWszystkieDaneOdWierszaDoWiersza(self, poczatek, koniec):
        x = 0
        result = []
        for record in self.data:
            if x >= poczatek and x <= koniec:
                result.append(record)
            x=x+1
        return result
        
    def zwrocWszystkieDaneDlaSkladowej(self, nazwaKolumny):
            daneDlaSkladowej = []
            for record in self.data:
                try:
                    daneDlaSkladowej.append(float(record[nazwaKolumny]))
                except: ValueError, "String value? Come on! Somemthing went wrong."
            return daneDlaSkladowej
            
    def dodajNowyWiersz(self, dane):
        print dane
        assert isinstance(dane, list),  ("Wrong parameter given in %s", self.dodajNowyWiersz.__name__)
        if(len(dane)==len(self.temp)):
            toAppend = {}
            for i in range(len(dane)):
                toAppend[self.temp[i]] = dane[i]
            self.data.append(toAppend)
        else:
            print "Missing paramters..."
            
    def dodajNowyAtrybut(self, atrybut, wartosc=0):
        assert isinstance(atrybut,str) , ("Wrong parameter given in %s", self.dodajNowyAtrybut.__name__)
        for dictionary in self.data:
            dictionary[atrybut] = wartosc
        
    def wypiszWszystkieWiersze(self):
        print self.data[0].keys()
        for record in self.data:
            temp = []
            for v in record.itervalues():
                temp.append(v)
            print temp
            
    def srednia(self, nazwaKolumny):
        srednia = 0.0
        try:
            for record in self.data:
                srednia+=float(record[nazwaKolumny])
                srednia = srednia/len(self.data)
        except: ValueError, "Wrong column name {0}".format(nazwaKolumny)
        return srednia
    
    def mediana(self, nazwaKolumny):
        if len(self.data)%2 == 1:
                return sorted(self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny))[(len(self.data)+1)/2]
        else:
                return (sorted(self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny))[(len(self.data))/2]+sorted(self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny))[((len(self.data))/2)+1])/2
    
    def minimum(self, nazwaKolumny):
        kolumny = self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny)
        return min(kolumny)
               
    def maksimum(self, nazwaKolumny):
        kolumny = self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny)
        return max(kolumny)
    
    def wariancja(self,nazwaKolumny):
        kolumny = self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny)
        os=0.0
        s = self.srednia(nazwaKolumny)
        try:
            for x in kolumny:
                os+=(x-s)**2.0
            os/=len(kolumny)
        except:
            pass
        return os
        
    def odchylenieStandardowe(self,nazwaKolumny):
        x = self.wariancja(nazwaKolumny)
        x**=0.5
        return x
    
    def normalizacja(self,nazwaKolumny):
        wartosci = self.zwrocWszystkieDaneDlaSkladowej(nazwaKolumny)
        wartoscSrednia = self.srednia(nazwaKolumny)
        odchylenieStandardowe = self.odchylenieStandardowe(nazwaKolumny)
        wartosciPoNormalizacji = []
        
        for element in wartosci:
            z = (element-wartoscSrednia)/odchylenieStandardowe
            wartosciPoNormalizacji.append(z)
            
        return wartosciPoNormalizacji
    
    #http://docs.scipy.org/doc/scipy/reference/spatial.distance.html
    def sklasyfikuj(self, numerWiersza, nazwaParametrow, liczbaSasiadow, metryka=MetrykaValues.EUCLIDES, parametrKlasyDecyzyjnej="RainTomorrow"):
        m = Metryka()
        
        testedValuesArray = [self.data[numerWiersza][i] for i in nazwaParametrow]
        testedValueCasted = [float(i) for i in testedValuesArray]
        
        alreadyFoundNeighbours = 0
        neighbourhoodArray = []
        
        data = None
        if metryka == MetrykaValues.EUCLIDES:

            for i in range (0,len(self.data)):
                if(alreadyFoundNeighbours == liczbaSasiadow):
                    break
                if i == numerWiersza:
                    continue
                testedValuesArray = [self.data[i][j] for j in nazwaParametrow]
                dist = m.metrykaEuklidesowa(testedValueCasted, [float(k) for k in testedValuesArray])
                neighbourhoodArray.append((dist,self.data[i][parametrKlasyDecyzyjnej]))
                
        
        elif metryka == MetrykaValues.MAHALANOBIS:
            
            for i in range (0,len(self.data)):
                if(alreadyFoundNeighbours == liczbaSasiadow):
                    break
                if i == numerWiersza:
                    continue
                testedValuesArray = [self.data[i][j] for j in nazwaParametrow]
                dist = m.metrykaMahalanobisa(testedValueCasted, [float(k) for k in testedValuesArray])
                neighbourhoodArray.append((dist,self.data[i][parametrKlasyDecyzyjnej]))
            
        elif metryka == MetrykaValues.MANHATAN:
            
            for i in range (0,len(self.data)):
                if(alreadyFoundNeighbours == liczbaSasiadow):
                    break
                if i == numerWiersza:
                    continue
                testedValuesArray = [self.data[i][j] for j in nazwaParametrow]
                print testedValuesArray
                dist = m.metrykaManhattan(testedValueCasted, [float(k) for k in testedValuesArray])
                print dist
                neighbourhoodArray.append((dist,self.data[i][parametrKlasyDecyzyjnej]))
                
        sorted_by_first = sorted(neighbourhoodArray, key=lambda tup: tup[0])
        
        d = {}
        for i in sorted_by_first[:liczbaSasiadow]:
            if i[1] in d:
                d[i[1]] +=1
            else:
                d[i[1]] = 0
        
        maxMember = None
        maxMemberCount = 0        
        for key in d:
            if d[key] > maxMemberCount:
                maxMemberCount = d[key]
                maxMember = key
            else:
                continue
        
        return (maxMember,maxMemberCount) #war1 -> klasadycyzyjna, #war2 -> ilosc najblizszych sasiadow z taka klasa
        
    #Algorytm k-NN
    
    #Ustalamy wartosc k (najlepiej liczbe nieparzysta, zwykle ok. 5-15).
    #Dla kazdego obiektu testowego o*:
        #-  wyznaczamy odleglosc r(o*,x) pomiedzy o* i kazdym obiektem treningowym x,
        #-  znajdujemy k obiektow treningowych najblizszych o*,
        #-  wsrod wartosci decyzji odpowiadajacych tym obiektom wykonujemy glosowanie,
        #-  najczesciej wystepujaca wartosc decyzji przypisujemy obiektowi o*.
        
    def jakoscKlasyfikacji(self,k, nazwaParametrow, numerWierszaTestowanego,parametrKlasyDecyzyjnej="RainTomorrow", metryka=MetrykaValues.EUCLIDES):
        
        m = Metryka()
        
        distances = []
        
        ilosc_poprawnie_zaliczonych = 0
        
        ilosc_elementow = len(self.data)
        
#         testedValuesArray = [self.data[numerWierszaTestowanego][i] for i in nazwaParametrow]
#         testedValueCasted = [float(i) for i in testedValuesArray]
    
#         assert len(numeryWierszyTreningowych) > 0, "Liczba elementow treningowych jest rowna 0"
#         
#         assert numerWierszaTestowanego not in numeryWierszyTreningowych, "Wiersz testowany nie moze byc w puli treningowej"
        
        sorted_by_second = None;
        
        currentValuesArray = [self.data[numerWierszaTestowanego][w] for w in nazwaParametrow]
        currentValueCasted = [float(h) for h in currentValuesArray]
        
        
        # Wszystkie oprocz jednego testowego w czesci treningowej
        loo = LeaveOneOut(len(self.data))
        
        #TODO: przerobic to zeby nie powielac tego samego kodu
        
        if(metryka==MetrykaValues.EUCLIDES):
            for train, test in loo:
                counter = 0
                for i in train:
                    print "Treningowa: {0} \n Testowa: {1}".format(train,test)
                    
                    counter+=1
                    
                    trainingValuesArray = [self.data[i][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaManhattan(currentValueCasted, trainingValueCasted)
                    distances.append((i,d));
                    
                    sorted_by_second = sorted(distances, key=lambda tup: tup[1])
            
                    di = {}
                    for i in sorted_by_second[:k]:
                        if i[1] in di:
                            di[i[1]] +=1
                        else:
                            di[i[1]] = 0
                    
                    maxMember = None
                    maxMemberCount = 0        
                    for key in di:
                        if di[key] > maxMemberCount:
                            maxMemberCount = di[key]
                            maxMember = key
                        else:
                            continue
                    
                for t in test:
                    trainingValuesArray = [self.data[t][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaEuklidesowa(currentValueCasted, trainingValueCasted)
                    
                    if(maxMember==float(self.data[t][parametrKlasyDecyzyjnej])):
                        ilosc_poprawnie_zaliczonych+=1  
                        print "Ilosc poprawnie zaliczonych elementow {0}".format(ilosc_poprawnie_zaliczonych)
           
                
        elif(metryka==MetrykaValues.MAHALANOBIS):
            for train, test in loo:
                counter = 0
                for i in train:
                    print "Treningowa: {0} \n Testowa: {1}".format(train,test)
                    
                    counter+=1
                    
                    trainingValuesArray = [self.data[i][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaManhattan(currentValueCasted, trainingValueCasted)
                    distances.append((i,d));
                    
                    sorted_by_second = sorted(distances, key=lambda tup: tup[1])
            
                    di = {}
                    for i in sorted_by_second[:k]:
                        if i[1] in di:
                            di[i[1]] +=1
                        else:
                            di[i[1]] = 0
                    
                    maxMember = None
                    maxMemberCount = 0        
                    for key in di:
                        if di[key] > maxMemberCount:
                            maxMemberCount = di[key]
                            maxMember = key
                        else:
                            continue
                    
                for t in test:
                    trainingValuesArray = [self.data[t][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaMahalanobisa(currentValueCasted, trainingValueCasted)
                    
                    if(maxMember==float(self.data[t][parametrKlasyDecyzyjnej])):
                        ilosc_poprawnie_zaliczonych+=1  
                        print "Ilosc poprawnie zaliczonych elementow {0}".format(ilosc_poprawnie_zaliczonych)
                        
        elif(metryka==MetrykaValues.MANHATAN):
            for train, test in loo:
                print "Treningowa: {0} \n Testowa: {1}".format(train,test)
                counter = 0
                for i in train:
                    #print train
                    
                    counter+=1
                    
                    trainingValuesArray = [self.data[i][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaManhattan(currentValueCasted, trainingValueCasted)
                    distances.append((i,d));
                    
                    sorted_by_second = sorted(distances, key=lambda tup: tup[1])
            
                    di = {}
                    for i in sorted_by_second[:k]:
                        if i[1] in di:
                            di[i[1]] +=1
                        else:
                            di[i[1]] = 0
                    
                    maxMember = None
                    maxMemberCount = 0        
                    for key in di:
                        if di[key] > maxMemberCount:
                            maxMemberCount = di[key]
                            maxMember = key
                        else:
                            continue
                    
                for t in test:
                    trainingValuesArray = [self.data[t][w] for w in nazwaParametrow]
                    trainingValueCasted = [float(h) for h in trainingValuesArray]
                    
                    d = m.metrykaManhattan(currentValueCasted, trainingValueCasted)
                    
                    if(maxMember==float(self.data[t][parametrKlasyDecyzyjnej])):
                        ilosc_poprawnie_zaliczonych+=1  
                        print "Ilosc poprawnie zaliczonych elementow {0}".format(ilosc_poprawnie_zaliczonych)
                                                            
        return ilosc_poprawnie_zaliczonych / float(len(self.data))
                
    def skip(self,iterable, at_start=0, at_end=0):
        it = iter(iterable)
        for x in itertools.islice(it, at_start):
            pass
        queue = collections.deque(itertools.islice(it, at_end))
        for x in it:
            queue.append(x)
            yield queue.popleft()          
    

        
if __name__ == "__main__":
    d = Data()
    d.loadFile("/Users/lukaszdworakowski/Documents/Aptana Studio 3 Workspace/SWD/Data/dane.csv")
    print d.sklasyfikuj(1, ["Temp3pm","Pressure9am","RelHumid9am"], 20, MetrykaValues.MANHATAN)
    print d.jakoscKlasyfikacji(10,["Temp3pm"], 2, "RainTomorrow", MetrykaValues.MANHATAN) * 100  
        
        
        
        