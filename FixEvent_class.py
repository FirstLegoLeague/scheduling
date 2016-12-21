# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:37:35 2016

@author: s129938
"""

class FixEvent():
    def __init__(self,name, eventID,start,stop,delay=0):
        self.name = name
        self.id = eventID
        self.start = start
        self.stop = stop
        self.delay = delay