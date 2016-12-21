# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 12:54:17 2016

@author: s129938
"""

class Table():
    def __init__(self,name,tableid,totTime,theType,delay = 0,minTeams =1, maxTeams=1):
        self.delay = delay
        self.name = name
        self.id = tableid
        self.totTime = totTime
        self.type = theType
        self.IDorder = []
        self.minTeams = minTeams
        self.maxTeams = maxTeams
        self.available = 0 #earliest time a new task can be added
        
    def assignTeam(self,teamID,teamName,start):
        self.IDorder.append((teamID,teamName,start,start + self.totTime))
        self.available = start + self.delay+self.totTime
    
    def assignFix(self, eventName,start,stop):
        self.IDorder.append((-1,eventName,start, stop))
        self.IDorder = sorted(self.IDorder, key=lambda x:x[2])