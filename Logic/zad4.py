'''
Created on 24-05-2014

@author: lukaszdworakowski
'''

from tree import *
from data import *

class drzewoDecyzyjne:
    def init(self):
        parts = 2
        firstLineWithParameterNames = 0
        
        d = Data()
        d.loadFile("../Data/iris.csv", wantSorted=True, index=0)
        parameters = d.reader[firstLineWithParameterNames]
        
        self.tree = Tree()
        self.tree.create_node("Root", "root")
        
        for i in parameters[:-1]:
            a = self.tree.create_node(i, i, parent = "root")
        
        parameterIndex = 0
        parameterIndexNested = 0
        
        for parameter in range(0,len(parameters)-1):
            
            if parameterIndex>0:
                d.loadFile("../Data/iris.csv", wantSorted=True, index=parameter)
                
            discretized = d.discretization(parts, parameterIndex)
            
            print discretized
            
            parameterName = parameters[parameter]
            
            temp = []
            for i in discretized:
                temp.append(i)        
                
            a = self.tree.create_node("mala",temp[0], parent = parameterName, elements=discretized[temp[0]])
            a = self.tree.create_node("duza",temp[1], parent = parameterName, elements=discretized[temp[1]])    
            
            parameterIndex += 1
            
            d.loadFile("../Data/iris.csv", wantSorted=True, index=parameterIndexNested)
            
            for parameterNested in range(0,len(parameters)-1):
            
                if parameterNested != parameter:
                    
                    if parameterIndexNested>0:
                        d.loadFile("../Data/iris.csv", wantSorted=True, index=parameterIndexNested)
                        
                    discretizedNested = d.discretization(parts, parameterIndexNested)
                    
                    parameterName = parameters[parameterNested]
                    
                    tempNested = []
                    for i in discretizedNested:
                        tempNested.append(" ".join(i))
                    
                    name = "NESTED" + parameterName
                    a = self.tree.create_node(name, name, parent = temp[0])
                    a = self.tree.create_node(name, name, parent = temp[1])
                    
            parameterIndexNested += 1
        return self
            
    def showMeTree(self):
        print("="*80)
        self.tree.show("root")
        print("="*80)
        
    def getTree(self):
        return self.tree


a = drzewoDecyzyjne().init()
a.showMeTree()

tree = a.getTree()
for node in tree.expand_tree("root", mode=1):
    print(node)
print("="*80)


