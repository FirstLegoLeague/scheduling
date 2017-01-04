# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:34:22 2016

@author: Tom Nijhof
"""
from __future__ import print_function,absolute_import
from Table_class import Table
from Team_class import Team
from FixEvent_class import FixEvent

class Schema():
    def __init__(self):
        self.teams = []
        self.tables = []
        self.fixEvents = []
        self.teamID = 0
        self.tableID = 0
        self.fixEventID = 0
        
    def assignTask(self,team, table, startTime):
        teamID = team.id
        tableID = table.id
        tableType = table.type
        #check if fixed event will interver
        stopTime = startTime+table.totTime+max(table.delay, team.delay)
        for i in self.fixEvents:
            if (startTime < i.start and  stopTime > i.start) or (startTime > i.start and startTime < i.stop):
                startTime = i.stop + i.delay
                break
        table.assignTeam(teamID=teamID, teamName=team.name, start=startTime)
        team.assignTabel(tableID=tableID, tableType=tableType,tableName = table.name,start = startTime, time=table.totTime)
        #print(table.available)
        #print(team.available,"\n")
        
    def makeSchema(self):
        allTabTypes = []
        for i in self.tables:
            allTabTypes.append(i.type)
        numTables = len(set(allTabTypes))
        for i in self.teams:
            i.changeNumtypes(numTables)
        completTables = []
        completTeams = []
        while True:
            self.teams = sorted(self.teams, key=lambda team:team.available)
            self.tables = sorted(self.tables, key=lambda tables:tables.available)
        
            theType = self.tables[0].type
            
            findOne = False
            for i in self.teams:
                if i.doneTables[theType] is False and self.tables[0].available >= i.available:
                    self.assignTask(i, self.tables[0],self.tables[0].available)
                    findOne = True
                    break
            
            
            if not findOne:
                tableComplet = True
                for j in self.teams:
                    if j.doneTables[theType] is False:
                        self.assignTask(j, self.tables[0],j.available)
                        tableComplet = False
                        break
                if tableComplet:
                    completTables.append(self.tables[0])
                    del self.tables[0]
        
            if len(self.tables) == 0:
                break
            complet = True
            for k in range(len(self.teams))[::-1]:
                if self.teams[k].complete == False:
                    complet = False
                else:
                    completTeams.append(self.teams[k])
                    del self.teams[k]
            if complet:
                break
        self.teams = sorted(completTeams+self.teams, key=lambda team:team.id)
        self.tables = sorted(completTables+self.tables, key=lambda tables:tables.id)
        for i in self.fixEvents:
            for j in self.teams:
                j.assignFix(eventName=i.name,start=i.start,stop=i.stop)
            for j in self.tables:
                j.assignFix(eventName=i.name,start=i.start,stop=i.stop)
        return("Schema made")
    
    def addTeam(self,name,delay):
        self.teams.append(Team(name,self.teamID,1,delay=delay))
        self.teamID += 1
    
    def addTable(self,name,totTime,typeT,delay):
        self.tables.append(Table(name,self.tableID,totTime=totTime,theType=typeT,delay=delay))
        self.tableID += 1
        
    def addFixEvent(self,name,start,stop):
        self.fixEvents.append(FixEvent(name,self.fixEventID,start=start,stop=stop))
        self.fixEventID += 1
    
    def removeTeam(self,ID):
        for i in range(len(self.teams)):
            if self.teams[i].id == ID:
                del self.teams[i]
                return("team %i is succesfully removed"%ID)
        return("team %i could not be found"%ID)
    
    def removeTable(self,ID):
        for i in range(len(self.tables)):
            if self.tables[i].id == ID:
                del self.tables[i]
                return("table %i is succesfully removed"%ID)
        return("table %i could not be found"%ID)
    
    def removeFixEvent(self,ID):
        for i in range(len(self.fixEvents)):
            if self.fixEvents[i].id == ID:
                del self.fixEvents[i]
                return("fix event %i is succesfully removed"%ID)
        return("fix event %i could not be found"%ID)
    
    def schemaTeam(self, ID):
         for i in range(len(self.teams)):
            if self.teams[i].id == ID:
                return(self.teams[i].IDorder)
                
    def schemaTable(self, ID):
         for i in range(len(self.tables)):
            if self.tables[i].id == ID:
                return(self.tables[i].IDorder)
                
    def schemaTotalTeam(self):
        total = []
        for i in self.teams:
            total.append((i.name, i.IDorder))
        return(total)
    
    def schemaTotalTable(self):
        total = []
        for i in self.tables:
            total.append((i.name, i.IDorder))
        return(total)
            
"""
==============
Test situation
==============
"""
'''
delayTable = 50
delayTeam = 70

s = Schema()
for i in range(7):
    s.addTeam("team"+str(i),delayTeam)
s.addTable("Table 0",200,0,delayTable)
s.addTable("Table 1",200,1,delayTable)
s.addTable("Table 2",150,2,delayTable)
s.addTable("Table 3a",250,3,delayTable)
s.addTable("Table 3b",250,3,delayTable)
s.addTable("Onzin",250,4,delayTable)
s.removeTable(5)
s.addFixEvent("Fix1",550,700)
s.addFixEvent("Fix2",900,1150)
s.makeSchema()
#'''