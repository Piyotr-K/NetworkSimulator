#!/usr/bin/python

from socket import * 

port = 8001
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))
print ("waiting on port: ", port)
data, addr = sockobj.recvfrom(1024)
print ("Received: ", data.decode('utf-8'), "From: ", addr)