import csv
import array
import string

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
    
    def loadFile(self, sciezka):
        with open(sciezka, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
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
                
    def zamianaWartosciTekstowychNaWartosciLiczbowe(self):
        zamiana = {}
        j = 0
        
        if self.data==None:
            assert self.data, "You should load data file first."
        
        with self.data as dicts:
            for lista in dicts:
                for i in list:
                    if(type(i) is str):
                        if(zamiana[i]==None):
                            zamiana[i] = j
                            lista[i] = j
                        else:
                            lista[i] = zamiana[i]
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
        