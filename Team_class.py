# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 12:55:21 2016

@author: s129938
"""

class Team():
    def __init__(self,name, teamid, numTypes,delay):
        self.name = name
        self.id = teamid
        self.delay = delay
        self.IDorder = []
        self.doneTables = [False]*numTypes
        self.available = 0#earliest time a new task can be added
        self.complete = False
        
    def assignTabel(self,tableID,tableName,tableType,start,time):
        self.IDorder.append((tableID,tableName,start, start +time))
        self.available = start + self.delay+time
        self.doneTables[tableType] = True
        if not (False in self.doneTables):
            self.complete = True
    
    def assignFix(self, eventName,start,stop):
        self.IDorder.append((-1,eventName,start, stop))
        self.IDorder = sorted(self.IDorder, key=lambda x:x[2])
        
    def changeNumtypes(self,n):
        self.doneTables = [False]*n