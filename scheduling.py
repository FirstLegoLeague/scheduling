# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:34:22 2016

@author: s129938
"""
import numpy as np

totalIDTeam = 0
totalIDTable = 0
delayTable = 50
delayTeam = 70
fixEvents = [("Fix1",500,700),("Fix2",900,1150)]
startTime = 100
stopTime = 2500

class tables():
    def __init__(self,name,totTime,theType=-1):
        global totalIDTable
        global delayTable
        self.name = name
        self.id = totalIDTable
        self.totTime = totTime
        self.type = theType
        self.IDorder = []
        self.available = 0 #earliest time a new task can be added
        totalIDTable += 1
        
    def assignTeam(self,teamID,start):
        self.IDorder.append((teamID,start))
        self.available = start + delayTable+self.totTime


#Examples
allTables = [tables("table 0", 200,0),tables("table 1", 200,1),tables("table 2", 150,2),tables("table 3a", 250,3),tables("table 3b", 250,3)]


"""
===========
Creat teams
===========
"""
allTypes = set()
for i in allTables:
    allTypes.add(i.type)
    
numTypes = len(allTypes)
class team():
    def __init__(self,name):
        global totalIDTeam
        global delayTeam
        global numTypes
        self.name = name
        self.id = totalIDTeam
        self.tables = []
        self.doneTables = [False]*numTypes
        self.available = 0#earliest time a new task can be added
        totalIDTeam += 1
        self.complete = False
        
    def assignTabel(self,tableID,tableType,start,time):
        self.tables.append((tableID,start, start +time))
        self.doneTables[tableType] = True
        self.available = start + delayTeam+time
        if not (False in self.doneTables):
            self.complete = True

#Examples
allTeams = [team("hello"),
            team("world"),
            team("haai"),
            team("mars"),
            team("hoi"),
            team("venus"),
            team("eenhoorn")]

"""
=================
Making the schema
=================
"""
def assignTask(team, table, startTime):
    teamID = team.id
    tableID = table.id
    tableType = table.type
    table.assignTeam(teamID, startTime)
    team.assignTabel(tableID=tableID, tableType=tableType,start = startTime, time=table.totTime)
  
completTables = []
completTeams = []
while True:
    allTeams = sorted(allTeams, key=lambda team:team.available)
    allTables = sorted(allTables, key=lambda tables:tables.available)

    theType = allTables[0].type
    
    findOne = False
    for i in allTeams:
        if i.doneTables[theType] is False and allTables[0].available >= i.available:
            assignTask(i, allTables[0],allTables[0].available)
            findOne = True
            break
    
    
    if not findOne:
        tableComplet = True
        for j in allTeams:
            if j.doneTables[theType] is False:
                assignTask(j, allTables[0],j.available)
                tableComplet = False
                break
        if tableComplet:
            completTables.append(allTables[0])
            del allTables[0]

    if len(allTables) == 0:
        break
    complet = True
    for k in range(len(allTeams))[::-1]:
        if allTeams[k].complete == False:
            complet = False
        else:
            completTeams.append(allTeams[k])
            del allTeams[k]


"""
============
Making a GUI
============
"""
completTeams = sorted(completTeams+allTeams, key=lambda team:team.id)
completTables = sorted(completTables+allTables, key=lambda tables:tables.id)

print("Table")
for i in completTables:
    print(i.IDorder)

print("Teams")
for i in completTeams:
    print(i.tables)