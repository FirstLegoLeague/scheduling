# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 17:43:39 2016

@author: s129938
"""
from __future__ import division,print_function,absolute_import

import socket
import re
import os
import time

class mhub_conc():
    def __init__(self,url, PORT):
        socket.setdefaulttimeout = 0.50
        os.environ['no_proxy'] = '127.0.0.1,localhost'
        self.linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
        self.CRLF = "\r\n\r\n"
        HOST = url  # The remote host
        # create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(10)

        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #s.setblocking(0)
        self.s.connect((HOST, PORT))

    def SEND(self,message):
        totMes = '{"type":"publish","node":"default","topic":"python_schema","data":"%s"}%s'%(message,self.CRLF)
        self.s.send(totMes.encode())
        
    def LISTEN(self):
        #DOESN'T WORK!!!
        self.s.settimeout(None)
        self.data = self.s.makefile()
        if self.data != b'':
            print(self.data)
        """
        self.data = self.s.recv(1)
        if self.data:
            print(self.data)
        #"""
        '''
        conn, address = self.s.accept()
        print(conn)
        print(address)
        #'''
    
    def shutdown(self):
        self.s.shutdown(1)
        self.s.close()


test = mhub_conc("localhost", 13900)
test.SEND("Websocket")
st = time.time()

test.LISTEN()
    #break