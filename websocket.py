# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 17:43:39 2016

@author: s129938
"""
from __future__ import division,print_function,absolute_import
import threading
import socket
import re
import os
import json
from scheduling import Schema

class mhub_conc():
    def __init__(self,url, PORT):
        socket.setdefaulttimeout = 0.50
        os.environ['no_proxy'] = '127.0.0.1,localhost'
        self.listLock = threading.Lock()
        self.printLock = threading.Lock()
        self.linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
        self.CRLF = "\r\n\r\n"
        HOST = url  # The remote host
        self.todoList = []
        self.schemaExc = False
        self.schemaAcc = False
        # create an INET, STREAMing socket
        self.l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST= HOST
        self.PORT = PORT
        self.l.connect((HOST, PORT))
        self.subscriptString = '{"type": "subscribe","node": "default"}%s'%(self.CRLF)
        self.l.send(self.subscriptString.encode())

    def SEND(self,typeMes,message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        s.settimeout(None)
        #self.s.settimeout(10)
        #totMes = '{"type":"publish","node":"default","topic":"python_schema","data":"%s"}%s'%(message,self.CRLF)
        totMes = '{"type":"publish","node": "default","topic":"schema_answer:%s","data":"%s"}%s'%(typeMes,message,self.CRLF)
        s.send(totMes.encode())
        s.close()
        
        
    def LISTEN(self):
        while True:
            self.data = self.l.makefile().readline()
            if self.data != '':
                inputData = json.loads(self.data)
                self.inputData = inputData
                topic = inputData['topic'].split(':')
                try:
                    data = inputData['data']
                except:
                    data = ''
                if topic[0] == "schema":
                    if len(topic)>1:
                        with self.listLock:
                            self.todoList.append((topic[1],data))
                    else:
                        with self.listLock:
                            self.todoList.append(("error","Error: expected in the form schema:ACTION"))
    def DOSTUFF(self):
        while True:
            if len(self.todoList) > 0:
                action = self.todoList[0][0]
                data = self.todoList[0][1]
                if action == "error":
                    self.SEND("error",data)
                elif action == "init":
                    #initialize
                    self.schema = Schema()
                    self.schemaExc = True
                elif action == "addTeam":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            name = str(d['name'])
                            delay = float(d['delay'])
                            self.schema.addTeam(name,delay)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To add a team you need to send in data {'name':str , 'delay':float}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "addTable":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            name = str(d['name'])
                            totalTime = float(d['time'])
                            theType = int(d['type'])
                            delay = float(d['delay'])
                            self.schema.addTable(name,totalTime,theType,delay)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To add a table you need to send in data {'name':str , 'time':float, 'type':int, 'delay':float}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "addFixEvent":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            name = str(d['name'])
                            start = float(d['start'])
                            stop = float(d['stop'])
                            self.schema.addFixEvent(name,start,stop)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To add a fixed event you need to send in data {'name':str , 'start':float, 'stop':float}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "delFixEvent":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            ID = str(d['id'])
                            self.schema.removeFixEvent(ID)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To delete a fixed event you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                
                elif action == "delTeam":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            ID = int(d['id'])
                            self.schema.removeTeam(ID)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To delete a team you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "delTable":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            ID = int(d['id'])
                            self.schema.removeTable(ID)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To delete a table you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "delFixEvent":
                    if self.schemaExc:
                        try:
                            d=json.loads(data)
                            ID = int(d['id'])
                            self.schema.removeFixEvent(ID)
                            self.schemaAcc = False
                        except:
                            self.SEND("error","To delete a fixed event you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "make":
                    if self.schemaExc:
                        self.schema.makeSchema()
                        self.schemaAcc = True
                    else:
                       self.SEND("error","The schema need to be initialize first, use schema:init")
                elif action == "getAllTeams":
                    if self.schemaAcc:
                        self.SEND("getAllTeams",str(self.schema.schemaTotalTeam()))
                    else:
                       self.SEND("error","The schema need to be made OR updated first, use schema:make")
                elif action == "getAllTables":
                    if self.schemaAcc:
                        self.SEND("getAllTables",str(self.schema.schemaTotalTable()))
                    else:
                       self.SEND("error","The schema need to be made OR updated first, use schema:make")
                elif action == "getOneTeam":
                    if self.schemaAcc:
                        try:
                            d=json.loads(data)
                            ID = int(d['id'])
                            self.SEND("getAllTables",str(self.schema.schemaTeam(ID)))
                        except:
                            self.SEND("error","To get a team schema you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be made OR updated first, use schema:make")
                elif action == "getOneTable":
                    if self.schemaAcc:
                        try:
                            d=json.loads(data)
                            ID = int(d['id'])
                            self.SEND("getAllTables",str(self.schema.schemaTable(ID)))
                        except:
                            self.SEND("error","To get a table schema you need to send in data {'id':int}")
                    else:
                       self.SEND("error","The schema need to be made OR updated first, use schema:make")
                else:
                    self.SEND("error","the command '%s' is not know"%action)
                
                del self.todoList[0]
    def shutdown(self):
        self.s.shutdown(1)
        self.s.close()


test = mhub_conc("localhost", 13902)


t = threading.Thread(target=test.LISTEN)
t.daemon = True
t.start()

t = threading.Thread(target=test.DOSTUFF)
t.daemon = True
t.start()
#'''

while True:
    1