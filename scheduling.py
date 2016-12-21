# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:34:22 2016

@author: Tom Nijhof
"""
from __future__ import print_function,absolute_import
from Table_class import Table
from Team_class import Team
from FixEvent_class import FixEvent

totalIDTeam = 0
totalIDTable = 0
delayTable = 50
delayTeam = 70


class Schema():
    def __init__(self,teams,tables, fixEvents):
        self.teams = teams
        self.tables = tables
        self.fixEvents = fixEvents
        
    def assignTask(self,team, table, startTime):
        teamID = team.id
        tableID = table.id
        tableType = table.type
        #check if fixed event will interver
        stopTime = startTime+table.totTime+max(delayTable, delayTeam)
        for i in self.fixEvents:
            if (startTime < i.start and  stopTime > i.start) or (startTime > i.start and startTime < i.stop):
                startTime = i.stop + i.delay
                break
        table.assignTeam(teamID=teamID, teamName=team.name, start=startTime)
        team.assignTabel(tableID=tableID, tableType=tableType,tableName = table.name,start = startTime, time=table.totTime)
        #print(table.available)
        #print(team.available,"\n")
        
    def makeSchema(self):
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
        self.schema()
    
    def schema(self):
        print("Table")
        for i in self.tables:
            print(i.IDorder)
        
        print("Teams")
        for i in self.teams:
            print(i.tables)
            
"""
==============
Test situation
==============
"""
exmpTables = [Table("table 0", 0,200,0, delay=delayTable),
              Table("table 1", 1,200,1, delay=delayTable),
              Table("table 2", 2,150,2, delay=delayTable),
              Table("table 3a", 3,250,3, delay=delayTable),
              Table("table 3b", 4,250,3, delay=delayTable)]

exmpTeams = [Team("hello",0, 4, delay=delayTeam),
            Team("world",1, 4, delay=delayTeam),
            Team("haai",2, 4, delay=delayTeam),
            Team("mars",3, 4, delay=delayTeam),
            Team("hoi",4, 4, delay=delayTeam),
            Team("venus",5, 4, delay=delayTeam),
            Team("eenhoorn",6, 4, delay=delayTeam)]

exmpFixEvents = [FixEvent("Fix1",0,550,700),
                 FixEvent("Fix2",1,900,1150)]

s = Schema(exmpTeams, exmpTables, exmpFixEvents)
s.makeSchema()