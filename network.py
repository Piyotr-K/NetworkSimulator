#!/usr/bin/python

from socket import *

port_recv = 8000
port_send = 8001
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockobj.bind(("", port_recv))
print ("waiting on port: ", port_recv)
data, addr = sockobj.recvfrom(1024)
print ("Received: ", data.decode('utf-8'), "From: ", addr)
sockobj.close()
sockobj = socket(AF_INET, SOCK_DGRAM)
print ("Sending: ", data.decode('utf-8'))
sockobj.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockobj.bind(("", port_send))