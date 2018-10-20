#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:16:20 2018

@author: Zhijie
"""

import networkx as nx
import matplotlib.pyplot as plt
import copy
import numpy as np
import random
import time
#import collections
intime=time.time()

def draw(n,k,p):#draw WS network
    #global n
    #G1=nx.karate_club_graph()#,seed=20180530)
    G1=nx.generators.random_graphs.watts_strogatz_graph(n, k, p)
    G2=copy.deepcopy(G1)
    U=nx.algorithms.operators.binary.disjoint_union(G1,G2)
    #n=len(G1)
    for i in range(n):
        U.add_edge(i, n+i)
    #nx.draw(U,with_labels=True)
    #plt.show()
    return U

def rewire(i1, i2, f2):
    U.remove_edge(i1,i2)
    U.add_edge(i1,f2)

#n=len(U)/2
#n=34
n=50
k=6
p=0.8

U= draw(n,k,p)

degreelist=[]
for site in range(2*n): degreelist.append(len(U.neighbors(site)))
totalnode=2*n

ne2J=-4

spin_array0=np.array(list(np.ones(n))+list(np.negative(np.ones(n))))

Ttrial=50000
temperature=5
deadline=400
rtime1=0

latewin=0
win=0

#windifference=12
#windifference=12
#negwindifference=-1*windifference
downrange=150
uprange=400
interval=int((uprange-downrange)/50)
#for tenT in range(20,161,5):
#    temperature=tenT/10

estore=[]
rawresult=[]
result=[]
for value in range(n):estore.append (np.exp((ne2J * value)/temperature))
for rtime in range (downrange,uprange+1,interval):
    
    #hist_difference=np.zeros(4*n)
    Gapi=[]
    Gapf=[]
    degreestore1=[]
    degreestore=[]
    counttrial=0
    
    while counttrial<Ttrial:
        
        if counttrial%500==0: 
           U = draw(n,k,p) 
           degreelist=[]
           for site in range(2*n): degreelist.append(len(U.neighbors(site)))
        #U = copy.deepcopy(U0)
        #spin_array=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])#copy.deepcopy(spin_array0)
        spin_array=copy.deepcopy(spin_array0)
        spy1=random.randint(0,n-1)
        spy2=random.randint(n,totalnode-1)
        
        #bestn1=spy1
        bestn=spy2
        
        step=0
        
        #bestd1=0
        bestd=len(U.neighbors(spy2)) #highest degree
        ichoice=list(range(0,totalnode))
        spychoice=list(range(n,totalnode))
        
        
        ichoice.remove(spy1)
        spin_array[spy1]=-1
        degreestore1.append(degreelist[spy1])
        
        if rtime == 0:
            ichoice.remove(spy2)
            spin_array[spy2]=1
            Gapi.append(np.sum(spin_array))
            
        evodegree=[bestd]

        while step<deadline:
            spinvalue=0
            step+=1
            if step<=rtime:      
                site=random.choice(spychoice)
                #degree=len(U.neighbors(site))
                degree=degreelist[site]
         
                if degree>=bestd:
                    evodegree.append(degree)
                    bestd=degree
                    bestn=site
                    
            
            if step==rtime:#spy2 flip node at response time only
                spy2=bestn
                spin_array[spy2]=1   
                ichoice.remove(spy2)
                Gapi.append(np.sum(spin_array))
                #rewire(site,random.choice(U.neighbors(site)),evodegree[0])
                
            
            i=random.choice(ichoice)  
            for node in U.neighbors(i): spinvalue+= spin_array[node]
            e = ne2J * spin_array[i] * spinvalue
            if e >= 0 or estore[int(abs(spinvalue))] > random.random():
                spin_array[i]*=-1
            
        counttrial+=1
        degreestore.append(bestd)
        Gapf.append(np.sum(spin_array)) 
        #Gapidict=collections.Counter(Gapi)
        #Gapfdict=collections.Counter(Gapf)
        #hist_difference[int(difference+2*n)]+=1
               
    rawresult.append([rtime,degreestore,degreestore1,Gapi,Gapf,temperature,deadline])#,Gapidict,Gapfdict])



#result=[]
#for item in rawresult:
 #   win=np.sum(item[-1][:int(2*n-windifference)])
  #  latewin=np.sum(item[-1][2*n+int(windifference):])           
   # result.append([item[0],item[1],latewin/Ttrial,win/Ttrial,windifference,deadline])
        
        
print("time used: ", time.time()-intime)
